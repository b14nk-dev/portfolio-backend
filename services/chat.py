import json
from collections.abc import Iterator

from groq.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)
from groq.types.chat.chat_completion_message_tool_call_param import (
    ChatCompletionMessageToolCallParam,
)

from llm import tools_dict
from llm.LLM import LLM
from utils.event_type import event_type


def start_new_chat(question: str) -> Iterator[str]:

    llm = LLM()
    llm.create_message({"role": "user", "content": question})

    yield event_type("status", stage="thinking")
    announced: set[str] = set()
    for _ in range(6):
        content: list[str] = []
        calls: dict[int, ChatCompletionMessageToolCallParam] = {}
        finish = None
        try:
            for chunk in llm.get_response():
                if not chunk.choices:
                    continue
                choice = chunk.choices[0]
                delta = choice.delta

                if delta.content:
                    content.append(delta.content)
                    yield event_type("token", text=delta.content)

                for tc in delta.tool_calls or []:
                    slot = calls.setdefault(
                        tc.index,
                        {
                            "id": "",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        },
                    )
                    if tc.id:
                        slot["id"] = tc.id
                    if tc.function:
                        if tc.function.name:
                            slot["function"]["name"] = tc.function.name
                        if tc.function.arguments:
                            slot["function"]["arguments"] += tc.function.arguments

                    if (
                        tc.function
                        and tc.function.name
                        and tc.function.name not in announced
                    ):
                        announced.add(tc.function.name)
                        yield event_type("status", stage="tool", name=tc.function.name)

                if choice.finish_reason:
                    finish = choice.finish_reason

            if finish != "tool_calls" or not calls:
                yield event_type("done")
                return

            assistant: ChatCompletionAssistantMessageParam = {
                "role": "assistant",
                "tool_calls": [calls[i] for i in sorted(calls)],
            }
            if content:
                assistant["content"] = "".join(content)
            llm.create_message(assistant)

            for call in assistant["tool_calls"]:
                try:
                    fn = tools_dict[call["function"]["name"]]
                    args = json.loads(call["function"]["arguments"] or "{}")
                    result = str(fn(**args))
                except Exception as exc:
                    result = f"Tool error: {exc}"

                llm.create_message(
                    {"role": "tool", "tool_call_id": call["id"], "content": result}
                )

        except Exception:
            yield event_type(
                "error", message="Something went wrong — please email Ritik directly."
            )
            yield event_type("done")
            return
    yield event_type("error", message="Sorry, I couldn't finish that answer.")
    yield event_type("done")
