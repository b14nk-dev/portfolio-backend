from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


class RateLimited(Exception):
    pass

@dataclass(frozen=True)
class RateLimit:
    retry_after: float | None = None

    def as_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


__all__ = ["RateLimit", "RateLimited"]
