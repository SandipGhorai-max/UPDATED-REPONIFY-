"""
main.py — FastAPI entry point for Reponify.

Zero business logic. Only wires up CORS, health check,
and the /analyze endpoint which calls the 3-layer pipeline in sequence.

Pipeline:
    Layer 1 (Vision)   → RepoDNA        [Cerebras llama3.1-8b]
    Layer 2 (Creative) → SetupGuide     [Cerebras gpt-oss-120b]

Run with: uvicorn main:app --reload --port 8000
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from cachetools import TTLCache

from config import settings
from models.schemas import AnalyzeRequest, ReponifyResponse
from layers.vision import run_vision
from layers.creative import run_creative
from utils.github import parse_github_url, GitHubAuthError, GitHubNotFoundError, close_http_client
from utils.logging_config import setup_logging
from utils.key_manager import github_token_rotator

# Configure structured JSON logging before anything else runs
setup_logging()
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Response cache
# 1-hour TTL, max 200 entries. Key = normalised github_url.
# ---------------------------------------------------------------------------
_analysis_cache: TTLCache = TTLCache(maxsize=200, ttl=3600)


def _cache_key(github_url: str, os: str, experience_level: str) -> str:
    """Generate a composite cache key from URL + OS + experience level."""
    normalized_url = github_url.strip().lower().rstrip("/")
    os_normalized = os.strip().lower()
    exp_normalized = experience_level.strip().lower()
    return f"{normalized_url}|{os_normalized}|{exp_normalized}"

# ---------------------------------------------------------------------------
# App lifespan (close pooled HTTP client on shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"[Reponify] Starting with:")
    print(f"  Cerebras keys:   4 loaded")
    print(f"  Vision model:    {settings.CEREBRAS_VISION_MODEL}")
    print(f"  Creative model:  {settings.CEREBRAS_CREATIVE_MODEL}")
    print(f"  GitHub tokens:   {github_token_rotator.count} loaded")
    print(f"  Rotation:        Immediate on any server error")
    print(f"  Retry policy:    No retry on same key. Rotate instantly.")
    logger.info("Reponify API starting up")
    yield
    await close_http_client()
    logger.info("Reponify API shut down cleanly")


app = FastAPI(title="Reponify API", version="1.0.0", lifespan=lifespan)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inject standard HTTP security headers on every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# List every origin that is allowed to call this API.
# Add your production domain here before deploying.
ALLOWED_ORIGINS = [
    "https://reponify.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,   # No cookies/sessions used — keep False
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept"],
)


@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html from the same origin as the API."""
    html_path = Path(__file__).parent / "index.html"
    return FileResponse(html_path, media_type="text/html")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0", "cache_size": len(_analysis_cache)}


# ---------------------------------------------------------------------------
# Pipeline helper
# ---------------------------------------------------------------------------

def _enforce_cd_after_clone(steps: list, github_url: str) -> list:
    """
    Hardcoded guarantee: cd always follows git clone.
    This runs after all AI layers as pure Python logic.
    AI cannot skip this step.
    """
    import re

    # Extract repo name from GitHub URL
    match = re.search(r'github\.com/[^/]+/([^/\s\.]+)', github_url)
    repo_name = match.group(1) if match else None

    if not repo_name:
        return steps

    result = []
    for i, step in enumerate(steps):
        result.append(step)
        command = step.command if hasattr(step, 'command') else step.get("command", "")

        # Check if this step is git clone
        if command.strip().startswith("git clone"):
            # Check if next step is already cd
            next_step = steps[i + 1] if i + 1 < len(steps) else None
            if next_step:
                next_cmd = next_step.command if hasattr(next_step, 'command') else next_step.get("command", "")
            else:
                next_cmd = ""

            if not next_cmd.strip().startswith("cd "):
                # Insert cd step immediately after git clone
                from models.schemas import SetupStep
                cd_step = SetupStep(
                    step_number=step.step_number + 1,
                    title=f"Enter the project folder",
                    command=f"cd {repo_name}",
                    what_it_does=f"Moves into the {repo_name} folder that was just downloaded.",
                    what_you_learn="After cloning, you must enter the folder before running any commands."
                )
                result.append(cd_step)

    # Renumber all steps sequentially
    for idx, step in enumerate(result):
        step.step_number = idx + 1

    return result


async def _run_pipeline(request: AnalyzeRequest) -> ReponifyResponse:
    """Execute the 2-layer analysis pipeline (Vision → Creative)."""

    # --- Validate the GitHub URL ---
    try:
        owner, repo = parse_github_url(request.github_url)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid GitHub URL: {request.github_url}. "
                   "Expected format: https://github.com/owner/repo",
        )

    logger.info("Pipeline started for %s/%s", owner, repo)

    # --- Layer 1: Repo Vision ---
    try:
        repo_dna, raw_readme = await run_vision(request.github_url, os=request.os)
    except GitHubAuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    except GitHubNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Repository not found: {owner}/{repo}",
        )
    except Exception as exc:
        logger.exception("Vision layer failed")
        raise HTTPException(status_code=500, detail=f"Vision layer failed: {str(exc)}")

    # --- Layer 2: Guide Generator (RepoDNA passed directly) ---
    try:
        setup_guide = await run_creative(
            repo_dna,
            os=request.os,
            experience_level=request.experience_level,
            github_url=request.github_url
        )
    except Exception as exc:
        logger.exception("Guide generation failed")
        raise HTTPException(status_code=500, detail=f"Guide generation failed: {str(exc)}")

    # --- Post-processing: guarantee cd after git clone (pure Python, no AI) ---
    setup_guide.setup_steps = _enforce_cd_after_clone(
        setup_guide.setup_steps,
        request.github_url
    )

    logger.info("Pipeline completed for %s/%s", owner, repo)
    return setup_guide


@app.post("/analyze", response_model=ReponifyResponse)
async def analyze_repo(request: AnalyzeRequest):
    """
    Analyze a public GitHub repository and return a complete setup guide.

    Pipeline:
        Layer 1 (Vision)   → RepoDNA        [Cerebras llama3.1-8b]
        Layer 2 (Creative) → SetupGuide     [Cerebras gpt-oss-120b]

    Results are cached for 1 hour per unique GitHub URL + OS + experience level.
    """
    cache_key = _cache_key(request.github_url, request.os, request.experience_level)

    # Return cached result if available
    if cache_key in _analysis_cache:
        logger.info("Cache hit for %s", cache_key)
        return _analysis_cache[cache_key]

    # Run the full pipeline with a hard timeout
    try:
        result = await asyncio.wait_for(
            _run_pipeline(request),
            timeout=60.0
        )
    except asyncio.TimeoutError:
        logger.error("Pipeline timed out for %s", cache_key)
        raise HTTPException(
            status_code=408,
            detail={
                "error": "Analysis timed out",
                "message": "This repository took too long to analyze. Try a smaller or simpler repository.",
                "timeout_seconds": 60
            }
        )

    _analysis_cache[cache_key] = result
    return result