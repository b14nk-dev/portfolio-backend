import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "knowledge"
MANIFEST = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))

UNITS = {u["id"]: u for u in MANIFEST["units"]}

CONTENT = {
    uid: (ROOT / u["path"]).read_text(encoding="utf-8") for uid, u in UNITS.items()
}


def get_knowledge(unit: str) -> str:
    content = CONTENT.get(unit)
    if content is None:
        return "Unknown unit. Valid units: " + ", ".join(CONTENT)
    return content
