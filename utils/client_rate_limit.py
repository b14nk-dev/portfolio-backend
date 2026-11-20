from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter

from utils.client_key import client_key
from utils.limiter_config import ENABLED, LIMIT

limiter = Limiter(
    key_func=client_key,
    headers_enabled=True,
    enabled=ENABLED,
)


def rate_limit_exceeded_handler(
    request: Request, _exc: Exception
) -> JSONResponse:
    response = JSONResponse(
        status_code=429,
        content={
            "detail": "You've reached the question limit. Please try again later."
        },
    )
    return request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )


__all__ = [
    "LIMIT",
    "client_key",
    "limiter",
    "rate_limit_exceeded_handler",
]
