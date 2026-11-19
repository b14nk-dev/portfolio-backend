import json


def event_type(event_type: str, **data) -> str:
    return json.dumps({"type": event_type, **data}, ensure_ascii=False) + "\n"
