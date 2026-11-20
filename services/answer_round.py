from collections.abc import Iterator

from llm.LLM import LLMClient
from services.events import rate_limit_event
from utils.event_type import write_event
from utils.extras_filter import ExtrasFilter
from utils.extras_parse import parse_extras


def answer_round(llm: LLMClient) -> Iterator[str]:
    extras = ExtrasFilter()

    for text in llm.get_response():
        safe = extras.feed(text)
        if safe:
            yield write_event("token", text=safe)

    tail, raw_extras = extras.finish()
    if tail:
        yield write_event("token", text=tail)

    followups, links = parse_extras(raw_extras)
    if followups:
        yield write_event("followups", items=followups)
    if links:
        yield write_event("links", items=links)

    limit = rate_limit_event(llm)
    if limit:
        yield limit

    yield write_event("done")


__all__ = ["answer_round"]
