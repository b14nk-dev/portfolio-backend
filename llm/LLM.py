import os

import httpx
from dotenv import load_dotenv
from groq import Groq, Stream
from groq.types.chat import ChatCompletionMessageParam
from groq.types.chat.chat_completion_chunk import ChatCompletionChunk

from llm.system_prompts import system_prompt

from .tools import TOOLS_SCHEMA

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL")


if not api_key:
    raise ValueError("No api key found")


class init_llm:
    client: Groq
    model: str
    messages: list[ChatCompletionMessageParam]

    def __init__(self, model: str) -> None:
        self.client = Groq(
            api_key=api_key, timeout=httpx.Timeout(30.0, connect=5.0), max_retries=2
        )
        self.model = model
        self.messages = []
        self.create_message({"role": "system", "content": system_prompt})

    def create_message(self, param: ChatCompletionMessageParam) -> init_llm:
        self.messages.append(param)
        return self

    def get_response(self) -> Stream[ChatCompletionChunk]:
        return self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
            temperature=0,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            max_tokens=500,
        )


def LLM() -> init_llm:

    if not model:
        raise ValueError("No model name found")
    return init_llm(model=model)
