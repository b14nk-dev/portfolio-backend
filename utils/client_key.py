from __future__ import annotations

from fastapi import Request
from slowapi.util import get_remote_address


def client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        first = forwarded.split(",", 1)[0].strip()
        if first:
            return first

    real_ip = request.headers.get("x-real-ip")
    if real_ip and real_ip.strip():
        return real_ip.strip()

    return get_remote_address(request)


__all__ = ["client_key"]
