import logging
import os
from collections.abc import Iterator

from dotenv import load_dotenv

from llm.gemini_client import MAX_OUTPUT_TOKENS, build_request
from llm.gemini_models import ModelPool
from llm.rate_limit import RateLimit, RateLimited
from llm.streaming import stream_with_fallback
from llm.system_prompts import system_prompt

load_dotenv()

logger = logging.getLogger(__name__)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No Gemini api key found")


class LLMClient:
    def __init__(self, models: list[str] | None = None) -> None:
        self.messages: list[dict[str, str]] = []
        self.pool = ModelPool(models or ())
        self.model = self.pool.ensure()
        self.rate_limit: RateLimit | None = None
        self.add_message("system", system_prompt)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def request(self):
        return build_request(self.messages, max_tokens=MAX_OUTPUT_TOKENS)

    def get_response(self) -> Iterator[str]:
        return stream_with_fallback(self)


def create_llm() -> LLMClient:
    preferred = [
        name.strip()
        for name in os.getenv("GEMINI_MODELS", "").split(",")
        if name.strip()
    ]
    return LLMClient(models=preferred or None)


__all__ = ["LLMClient", "RateLimited", "create_llm"]
