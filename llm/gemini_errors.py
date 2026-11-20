from __future__ import annotations

import re
from typing import Any

_DELAY = re.compile(r"(\d+(?:\.\d+)?)s?")


class GeminiError(Exception):
    def __init__(
        self,
        status: int,
        message: str,
        retry_after: float | None = None,
        daily: bool = False,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
        self.retry_after = retry_after
        self.daily = daily

    @property
    def model_missing(self) -> bool:
        return self.status == 404 or (
            self.status == 400 and "model" in self.message.lower()
        )


def _seconds(value: Any) -> float | None:
    if not value:
        return None
    match = _DELAY.fullmatch(str(value).strip())
    return float(match.group(1)) if match else None


def _error_body(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    error = payload.get("error")
    return error if isinstance(error, dict) else payload


def parse_error(code: int, payload: Any, retry_header: Any = None) -> GeminiError:
    body = _error_body(payload)
    message = str(body.get("message") or f"Gemini request failed ({code})")
    retry = _seconds(retry_header)
    daily = "per day" in message.lower() or "perday" in message.lower()

    for detail in body.get("details") or []:
        kind = str(detail.get("@type", ""))
        if kind.endswith("RetryInfo"):
            retry = retry or _seconds(detail.get("retryDelay"))
        if kind.endswith("QuotaFailure"):
            for violation in detail.get("violations") or []:
                quota = str(violation.get("quotaId", "")).lower()
                if "perday" in quota:
                    daily = True

    return GeminiError(code, message, retry, daily)


def _retry_header(exc: Any) -> Any:
    headers = getattr(getattr(exc, "response", None), "headers", None)
    return headers.get("retry-after") if headers is not None else None


def from_api_error(exc: Any) -> GeminiError:
    return parse_error(
        int(getattr(exc, "code", 0) or 0),
        getattr(exc, "details", None),
        _retry_header(exc),
    )


__all__ = ["GeminiError", "from_api_error", "parse_error"]
