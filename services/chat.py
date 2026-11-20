import logging
from collections.abc import Iterator

from llm.LLM import RateLimited, create_llm
from services.answer_round import answer_round
from services.events import (
    GENERIC_FAILED,
    INIT_FAILED,
    USAGE_LIMITED,
    failure_events,
)
from services.prompting import reference_prompt
from services.special_friends import special_reply
from utils.event_type import write_event

logger = logging.getLogger(__name__)


def start_new_chat(question: str) -> Iterator[str]:
    yield write_event("status", stage="thinking")

    fixed_reply = special_reply(question)
    if fixed_reply:
        yield write_event("token", text=fixed_reply)
        yield write_event("done")
        return

    try:
        llm = create_llm()
    except Exception:
        logger.exception("could not initialise the LLM")
        yield from failure_events(None, INIT_FAILED)
        return

    llm.add_message("user", reference_prompt(question))

    try:
        yield from answer_round(llm)
    except RateLimited:
        yield from failure_events(llm, USAGE_LIMITED)
        return
    except Exception:
        logger.exception("chat request failed")
        yield from failure_events(llm, GENERIC_FAILED)
