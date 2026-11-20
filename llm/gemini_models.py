from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class GeminiModel:
    id: str
    requests_per_minute: int
    requests_per_day: int
    note: str


FREE_TIER: tuple[GeminiModel, ...] = (
    GeminiModel("gemini-3.5-flash-lite", 15, 500, "best balance"),
    GeminiModel("gemini-3.1-flash-lite", 15, 500, "previous Flash-Lite"),
    GeminiModel("gemini-3.8-flash", 5, 20, "newest Flash, small quota"),
    GeminiModel("gemini-3.6-flash", 5, 20, "previous Flash, small quota"),
    GeminiModel("gemma-4-31b-it", 30, 14_400, "largest daily quota"),
)


class ModelPool:
    DEFAULT_RPM = 10

    def __init__(self, preferred: Iterable[str] = ()) -> None:
        names = [name.strip() for name in preferred if name.strip()]
        self._candidates = list(dict.fromkeys(names)) or [m.id for m in FREE_TIER]
        self._tried: set[str] = set()
        self._dead: set[str] = set()
        self._current: str | None = self._candidates[0] if self._candidates else None

    @property
    def current(self) -> str | None:
        return self._current

    def rpm(self, model_id: str) -> int:
        for model in FREE_TIER:
            if model.id == model_id:
                return model.requests_per_minute
        return self.DEFAULT_RPM

    def ensure(self) -> str:
        if self._current is None:
            raise RuntimeError("No Gemini model is configured")
        return self._current

    def advance(self) -> bool:
        if self._current is not None:
            self._tried.add(self._current)
        self._current = self._next_untried()
        return self._current is not None

    def mark_dead(self, model_id: str | None) -> None:
        if model_id:
            self._dead.add(model_id)

    def reset(self) -> str | None:
        self._tried.clear()
        self._current = self._next_untried()
        return self._current

    def _next_untried(self) -> str | None:
        for model_id in self._candidates:
            if model_id not in self._tried and model_id not in self._dead:
                return model_id
        return None


__all__ = ["FREE_TIER", "GeminiModel", "ModelPool"]
