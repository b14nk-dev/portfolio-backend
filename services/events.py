from collections.abc import Iterator

from llm.LLM import LLMClient
from utils.event_type import write_event

INIT_FAILED = "Something went wrong — please email Ritik directly."
GENERIC_FAILED = "Something went wrong — please email Ritik directly."
USAGE_LIMITED = (
    "I'm at my usage limit right now — please try again in a few minutes."
)


def rate_limit_event(llm: LLMClient | None) -> str | None:
    info = llm.rate_limit if llm is not None else None
    if info is None:
        return None
    return write_event("rate_limit", **info.as_dict())


def failure_events(llm: LLMClient | None, message: str) -> Iterator[str]:
    limit = rate_limit_event(llm)
    if limit:
        yield limit
    yield write_event("error", message=message)
    yield write_event("done")


__all__ = [
    "GENERIC_FAILED",
    "INIT_FAILED",
    "USAGE_LIMITED",
    "failure_events",
    "rate_limit_event",
]
