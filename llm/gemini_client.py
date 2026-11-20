from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

from google import genai
from google.genai import errors, types

from .gemini_errors import GeminiError, from_api_error

MAX_OUTPUT_TOKENS = 1600
TIMEOUT_MS = 60_000

_client: genai.Client | None = None
Message = dict[str, str]


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY", ""),
            http_options=types.HttpOptions(
                timeout=TIMEOUT_MS,
                retry_options=types.HttpRetryOptions(attempts=1),
            ),
        )
    return _client


def build_request(
    messages: list[Message], max_tokens: int = MAX_OUTPUT_TOKENS
) -> tuple[list[types.Content], types.GenerateContentConfig]:
    system = [m["content"] for m in messages if m["role"] == "system"]
    contents = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
        if m["role"] != "system"
    ]
    config = types.GenerateContentConfig(
        system_instruction="\n\n".join(system) or None,
        temperature=0,
        max_output_tokens=max_tokens,
    )
    return contents, config


def _blocked(chunk: Any) -> bool:
    feedback = getattr(chunk, "prompt_feedback", None)
    return bool(getattr(feedback, "block_reason", None))


def stream_completion(
    model: str,
    contents: list[types.Content],
    config: types.GenerateContentConfig,
) -> Iterator[str]:
    try:
        stream = _get_client().models.generate_content_stream(
            model=model, contents=contents, config=config
        )
        for chunk in stream:
            if _blocked(chunk):
                raise GeminiError(400, "Gemini blocked the prompt")
            if chunk.text:
                yield chunk.text
    except errors.APIError as exc:
        raise from_api_error(exc) from exc


__all__ = ["build_request", "stream_completion"]
