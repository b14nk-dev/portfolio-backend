from __future__ import annotations

import time
from collections import deque

WINDOW = 60.0


class Pacer:
    def __init__(self, window: float = WINDOW) -> None:
        self.window = window
        self._hits: dict[str, deque[float]] = {}

    def _recent(self, model: str, now: float) -> deque[float]:
        hits = self._hits.setdefault(model, deque())
        while hits and now - hits[0] >= self.window:
            hits.popleft()
        return hits

    def wait(self, model: str, rpm: int) -> float:
        if rpm <= 0:
            return 0.0
        now = time.monotonic()
        hits = self._recent(model, now)
        if len(hits) < rpm:
            return 0.0
        return max(0.0, self.window - (now - hits[0]))

    def record(self, model: str) -> None:
        now = time.monotonic()
        self._recent(model, now).append(now)


PACER = Pacer()

__all__ = ["PACER", "Pacer", "WINDOW"]
