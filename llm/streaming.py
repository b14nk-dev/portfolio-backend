from __future__ import annotations

import logging
import time
from collections.abc import Iterator

from .gemini_client import GeminiError, stream_completion
from .pace import PACER
from .rate_limit import RateLimited, RateLimit

logger = logging.getLogger(__name__)

MAX_WAIT = 30.0

MAX_PACE = 10.0


def _pace(llm) -> None:
    wait = PACER.wait(llm.model, llm.pool.rpm(llm.model))
    if wait > MAX_PACE:
        raise RateLimited
    if wait:
        logger.info("pacing %s for %.1fs", llm.model, wait)
        time.sleep(wait)
    PACER.record(llm.model)


def _switch(llm) -> bool:
    if not llm.pool.advance():
        return False
    llm.model = llm.pool.current or llm.model
    logger.warning("switching to Gemini model %s", llm.model)
    return True


def _retryable(exc: GeminiError) -> bool:
    return exc.model_missing or exc.status >= 500


def stream_with_fallback(llm) -> Iterator[str]:
    delays: list[float] = []
    waited = False

    while True:
        _pace(llm)
        emitted = False
        contents, config = llm.request()
        try:
            for text in stream_completion(llm.model, contents, config):
                emitted = True
                yield text
            return
        except GeminiError as exc:
            if emitted:
                raise

            if exc.retry_after is not None:
                llm.rate_limit = RateLimit(retry_after=exc.retry_after)

            if exc.status == 429 or exc.daily:
                if exc.daily:
                    llm.pool.mark_dead(llm.model)
                elif exc.retry_after is not None:
                    delays.append(exc.retry_after)

                if _switch(llm):
                    continue
                if waited or not delays:
                    raise RateLimited from exc

                delay = min(min(delays), MAX_WAIT)
                logger.warning("all Gemini models limited; retrying in %.1fs", delay)
                time.sleep(delay)
                waited = True
                nxt = llm.pool.reset()
                if nxt is None:
                    raise RateLimited from exc
                llm.model = nxt
                continue

            if _retryable(exc) and _switch(llm):
                continue
            raise


__all__ = ["stream_with_fallback"]
