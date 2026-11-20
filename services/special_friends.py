import json
import os
import re

from dotenv import load_dotenv

load_dotenv()

def load_replies() -> dict[str, str]:
    try:
        values = json.loads(os.getenv("SPECIAL_FRIENDS_JSON", "{}"))
    except json.JSONDecodeError:
        return {}

    if not isinstance(values, dict):
        return {}
    return {
        str(name).strip().lower(): str(reply)
        for name, reply in values.items()
        if str(name).strip() and str(reply).strip()
    }



FRIEND_REPLIES = load_replies()
FRIEND_NAMES = "|".join(re.escape(name) for name in FRIEND_REPLIES)
INTRODUCTION = (
    re.compile(
        rf"\b(?:i am|i'm|im|my name is|this is)\s+({FRIEND_NAMES})\b",
        re.IGNORECASE,
    )
    if FRIEND_NAMES
    else None
)


def special_reply(question: str) -> str | None:
    text = question.strip().lower()
    if text in FRIEND_REPLIES:
        return FRIEND_REPLIES[text]

    if INTRODUCTION is None:
        return None

    match = INTRODUCTION.search(text)
    if match:
        return FRIEND_REPLIES[match.group(1).lower()]
    return None
