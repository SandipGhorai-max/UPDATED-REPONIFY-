"""
utils/logging_config.py — Structured JSON logging for Reponify.

Call setup_logging() once in main.py at startup.
Every module then does:
    import logging
    logger = logging.getLogger(__name__)
"""

import logging
import json
import sys
from datetime import datetime, timezone


class _JSONFormatter(logging.Formatter):
    """Emit each log record as a single-line JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Attach exception info when present
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure root logger with JSON output to stdout.
    Call once at application startup (main.py).
    Silences noisy third-party loggers that aren't useful in production.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JSONFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    # Remove any default handlers first
    root.handlers.clear()
    root.addHandler(handler)

    # Quiet down noisy third-party libraries
    for noisy in ("httpx", "httpcore", "hpack", "asyncio"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
