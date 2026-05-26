"""
utils/github.py — GitHub REST API client for Reponify.

Handles all GitHub data fetching: README, file tree, repo metadata,
package/dependency files, and .env.example detection.

Production hardening applied:
  - Module-level pooled httpx.AsyncClient (T2-3)
  - Exponential backoff retry on 429 / 5xx (T2-2)
  - Structured logging via logging module (T2-1)
"""

import re
import base64
import asyncio
import logging
import httpx

from config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom exceptions for clear error propagation
# ---------------------------------------------------------------------------

class GitHubAuthError(Exception):
    """Raised when GitHub returns 401/403 — invalid or missing token."""
    pass

class GitHubNotFoundError(Exception):
    """Raised when the repository genuinely does not exist (404)."""
    pass

class GitHubAPIError(Exception):
    """Raised for any other GitHub API failure."""
    pass


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_github_url(url: str) -> tuple[str, str]:
    """
    Extract (owner, repo) from a GitHub URL.
    Supports:
      https://github.com/owner/repo
      https://github.com/owner/repo.git
      https://github.com/owner/repo/tree/main/...

    SSRF protections:
      - Must start with https://github.com/ (re.match, not re.search)
      - Blocks @ in URL (credential injection / redirect tricks)
      - Owner and repo restricted to valid GitHub character set
    """
    url = url.strip().rstrip("/")

    # Block URLs with embedded auth credentials (e.g. https://user@github.com/...)
    if "@" in url:
        raise ValueError(
            "Invalid GitHub URL: authentication credentials are not allowed."
        )

    # Anchored match — must literally start with https://github.com/
    # Restricts owner/repo to alphanumerics, hyphens, underscores, dots only
    pattern = r"^https://github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)"
    match = re.match(pattern, url)
    if not match:
        raise ValueError(
            f"Invalid GitHub URL: '{url}'. "
            "Expected format: https://github.com/owner/repo"
        )

    owner = match.group(1)
    repo = match.group(2).removesuffix(".git")
    return owner, repo


# ---------------------------------------------------------------------------
# Pooled HTTP client  (T2-3)
# ---------------------------------------------------------------------------

_http_client: httpx.AsyncClient | None = None


def _get_http_client() -> httpx.AsyncClient:
    """Return the shared async client, creating it on first use."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=30,
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
            ),
        )
    return _http_client


async def close_http_client() -> None:
    """Cleanly close the shared client on app shutdown."""
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        logger.info("GitHub HTTP client closed")


# ---------------------------------------------------------------------------
# Async HTTP helpers
# ---------------------------------------------------------------------------

from utils.key_manager import github_token_rotator

def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _is_github_rate_limit(resp: httpx.Response) -> bool:
    if resp.status_code == 429:
        return True
    if resp.status_code == 403 and "rate limit" in resp.text.lower():
        return True
    if resp.headers.get("X-RateLimit-Remaining") == "0":
        return True
    return False


async def _get(path: str, _retries: int = 3) -> dict | list | None:
    """
    Fire a GET request against the GitHub REST API.  (T2-2 + T2-3)
    - Uses the pooled client.
    - Retries up to _retries times on 5xx with exponential backoff.
    - Rotates tokens on rate limits (429, 403 rate limit, or 0 remaining).
    Returns parsed JSON, or None on 404.
    Raises specific exceptions for 401/403 and other errors.
    """
    url = f"{settings.GITHUB_API_BASE}{path}"
    client = _get_http_client()

    tokens_to_try = github_token_rotator.count
    github_token_rotator.reset_index()

    for _ in range(tokens_to_try):
        current_token = github_token_rotator.get_current()
        current_token_idx = github_token_rotator.index
        
        for attempt in range(1, _retries + 1):
            resp = await client.get(url, headers=_headers(current_token))

            if resp.status_code == 404:
                return None

            if _is_github_rate_limit(resp):
                new_token = github_token_rotator.rotate()
                new_token_idx = github_token_rotator.index
                print(f"[GitHub] Rate limit hit. Rotating token {current_token_idx} → {new_token_idx}")
                break  # Break out of the retry loop to try the new token

            if resp.status_code in (401, 403):
                raise GitHubAuthError(
                    f"GitHub authentication failed (HTTP {resp.status_code}). "
                    "Check your GITHUB_TOKEN in .env — it may be invalid or expired."
                )

            # Transient server error — back off and retry
            if resp.status_code >= 500:
                retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
                logger.warning(
                    "GitHub API returned %s on %s — retrying in %ss (attempt %s/%s)",
                    resp.status_code, path, retry_after, attempt, _retries,
                )
                if attempt < _retries:
                    await asyncio.sleep(retry_after)
                    continue
                # Exhausted retries
                raise GitHubAPIError(
                    f"GitHub API unavailable after {_retries} retries "
                    f"(last status: {resp.status_code})"
                )

            resp.raise_for_status()
            return resp.json()

    raise GitHubAPIError("[GitHub] All GitHub tokens exhausted due to rate limits.")


# ---------------------------------------------------------------------------
# Public fetch functions
# ---------------------------------------------------------------------------

async def fetch_readme(owner: str, repo: str) -> str:
    """Fetch the decoded README content. Returns empty string if missing."""
    try:
        data = await _get(f"/repos/{owner}/{repo}/readme")
        if data and "content" in data:
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return content[:12000]
        return ""
    except GitHubAuthError:
        raise  # Let auth errors bubble up — don't swallow them
    except Exception as exc:
        logger.error("Failed to fetch README for %s/%s: %s", owner, repo, exc)
        return ""


async def fetch_file(owner: str, repo: str, path: str) -> str | None:
    """Fetch a single file's decoded content. Returns None if not found."""
    try:
        data = await _get(f"/repos/{owner}/{repo}/contents/{path}")
        if data and "content" in data:
            return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        return None
    except GitHubAuthError:
        raise
    except Exception as exc:
        logger.error("Failed to fetch file %s from %s/%s: %s", path, owner, repo, exc)
        return None


async def fetch_tree(owner: str, repo: str) -> list[str]:
    """
    Fetch the full recursive file tree.
    Returns a list of file paths (blobs only, no directories).
    Prioritizes root files, then src/app/lib, then others. Caps at 400 files.
    """
    try:
        repo_data = await _get(f"/repos/{owner}/{repo}")
        if not repo_data:
            return []
        default_branch = repo_data.get("default_branch", "main")

        tree_data = await _get(
            f"/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
        )
        if not tree_data or "tree" not in tree_data:
            return []

        files = [
            item["path"]
            for item in tree_data["tree"]
            if item.get("type") == "blob"
        ]

        def tree_sort_key(p: str):
            if "/" not in p:
                return 0
            if p.startswith("src/") or p.startswith("app/") or p.startswith("lib/"):
                return 1
            return 2

        return sorted(files, key=tree_sort_key)[:400]
    except GitHubAuthError:
        raise
    except Exception as exc:
        logger.error("Failed to fetch file tree for %s/%s: %s", owner, repo, exc)
        return []


async def fetch_repo_meta(owner: str, repo: str) -> dict:
    """Fetch repository metadata (name, description, stars, language, topics)."""
    try:
        data = await _get(f"/repos/{owner}/{repo}")
        if not data:
            return {}
        return {
            "name": data.get("name", ""),
            "description": data.get("description") or "No description provided",
            "language": data.get("language") or "Unknown",
            "stars": data.get("stargazers_count", 0),
            "topics": data.get("topics", []),
            "default_branch": data.get("default_branch", "main"),
        }
    except GitHubAuthError:
        raise
    except Exception as exc:
        logger.error("Failed to fetch repo metadata for %s/%s: %s", owner, repo, exc)
        return {}


# ---------------------------------------------------------------------------
# Package file detection
# ---------------------------------------------------------------------------

KNOWN_PACKAGE_FILES = [
    "package.json",
    "requirements.txt",
    "Cargo.toml",
    "pom.xml",
    "go.mod",
    "Gemfile",
    "composer.json",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "build.gradle",
]

ENV_FILES = [".env.example", ".env.sample", ".env.template", ".env.local.example"]
DOCKER_FILES = ["docker-compose.yml", "docker-compose.dev.yml", "docker-compose.prod.yml", "docker-compose.local.yml", "Dockerfile"]
SCRIPT_FILES = ["install.sh", "setup.sh", "bootstrap.sh", "Makefile"]


async def fetch_release_installers(owner: str, repo: str, os: str) -> list[dict]:
    """
    Check GitHub Releases API for direct download packages
    matching the user's OS. Returns a list of installer dicts.
    """
    WINDOWS_EXTS = [".exe", ".msi", ".msix"]
    MAC_EXTS = [".dmg", ".pkg"]
    LINUX_EXTS = [".deb", ".rpm", ".appimage", ".snap"]

    os_lower = os.lower()
    if "windows" in os_lower:
        target_exts = WINDOWS_EXTS
        platform = "windows"
    elif "mac" in os_lower:
        target_exts = MAC_EXTS
        platform = "macos"
    else:
        target_exts = LINUX_EXTS
        platform = "linux"

    try:
        data = await _get(f"/repos/{owner}/{repo}/releases/latest")
        if not data:
            return []

        assets = data.get("assets", [])
        installers = []

        for asset in assets:
            name = asset.get("name", "").lower()
            download_url = asset.get("browser_download_url", "")

            for ext in target_exts:
                if name.endswith(ext):
                    installers.append({
                        "platform": platform,
                        "filename": asset.get("name", ""),
                        "download_url": download_url,
                        "file_type": ext,
                    })
                    break

        return installers
    except GitHubAuthError:
        raise
    except Exception as exc:
        logger.error("Failed to fetch release installers for %s/%s: %s", owner, repo, exc)
        return []


async def fetch_all_repo_data(owner: str, repo: str) -> dict:
    """
    Master function — fetches everything needed for Layer 1 in parallel-ish fashion.
    Returns a dict with: readme, tree_str, meta, package_files, env_files, docker_files, script_files.
    Raises GitHubAuthError immediately if the token is bad.
    """
    import asyncio

    # First, do a quick auth check with the metadata call
    # If the token is bad, this will raise GitHubAuthError immediately
    meta = await fetch_repo_meta(owner, repo)

    # If meta is empty dict AND no auth error was raised, repo genuinely doesn't exist
    if not meta:
        raise GitHubNotFoundError(f"Repository {owner}/{repo} not found on GitHub.")

    # Now fetch the rest in parallel
    readme_task = asyncio.create_task(fetch_readme(owner, repo))
    tree_task = asyncio.create_task(fetch_tree(owner, repo))

    readme, tree = await asyncio.gather(
        readme_task, tree_task
    )

    tree_str = "\n".join(tree)[:8000]

    packages = []
    envs = []
    dockers = []
    scripts = []

    for path in tree:
        if path in KNOWN_PACKAGE_FILES and len(packages) < 8:
            packages.append(path)
        elif path in ENV_FILES:
            envs.append(path)
        elif path in DOCKER_FILES:
            dockers.append(path)
        elif path in SCRIPT_FILES:
            scripts.append(path)

    files_to_fetch = packages + envs + dockers + scripts
    
    package_contents: dict[str, str] = {}
    env_contents: dict[str, str] = {}
    docker_contents: dict[str, str] = {}
    script_contents: dict[str, str] = {}

    if files_to_fetch:
        fetch_tasks = [fetch_file(owner, repo, p) for p in files_to_fetch]
        results = await asyncio.gather(*fetch_tasks)

        total_package_chars = 0

        for path, content in zip(files_to_fetch, results):
            if content is None:
                continue

            if path in packages:
                content = content[:4000]
                if total_package_chars + len(content) > 32000:
                    content = content[:32000 - total_package_chars]
                if content:
                    package_contents[path] = content
                    total_package_chars += len(content)
            elif path in envs:
                env_contents[path] = content[:2000]
            elif path in dockers:
                docker_contents[path] = content[:3000]
            elif path in scripts:
                script_contents[path] = content[:3000]

    return {
        "readme": readme,
        "tree_str": tree_str,
        "meta": meta,
        "package_files": package_contents,
        "env_files": env_contents,
        "docker_files": docker_contents,
        "script_files": script_contents,
    }