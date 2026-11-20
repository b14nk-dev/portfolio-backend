from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def _settings() -> tuple[str, bool]:
    raw = os.getenv("CLIENT_RATE_LIMIT", "10").strip()
    head = raw.split("/", 1)[0].strip()
    try:
        count = int(head)
    except ValueError:
        count = 10

    if count <= 0:
        return "1/second", False
    if not raw:
        return "10/day", True
    if any(char.isalpha() for char in raw) or "/" in raw:
        return raw, True

    window = _env_float("CLIENT_RATE_WINDOW", 86400.0)
    if window == 60:
        return f"{raw}/minute", True
    if window == 3600:
        return f"{raw}/hour", True
    if window == 86400:
        return f"{raw}/day", True
    return f"{raw}/{window:g} seconds", True


LIMIT, ENABLED = _settings()

__all__ = ["ENABLED", "LIMIT"]
