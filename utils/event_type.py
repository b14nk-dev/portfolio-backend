import json


def write_event(name: str, **data) -> str:
    return json.dumps({"type": name, **data}, ensure_ascii=False) + "\n"
