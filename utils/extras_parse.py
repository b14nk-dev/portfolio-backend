from __future__ import annotations

import json
from typing import Any

from utils.extras_links import _clean_links


def _strip_fence(text: str) -> str:
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _clean_followups(value: Any) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []

    out: list[str] = []
    seen: set[str] = set()
    for item in value:
        if isinstance(item, dict):
            item = item.get("question") or item.get("text") or ""
        text = str(item).strip().lstrip("-•").strip().strip("\"'")
        text = " ".join(text.split())
        if not text or len(text) > 140:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(text)
        if len(out) >= 4:
            break
    return out


def parse_extras(raw: str) -> tuple[list[str], list[dict[str, str]]]:
    if not raw.strip():
        return [], []

    try:
        data = json.loads(_strip_fence(raw))
    except (json.JSONDecodeError, TypeError):
        return [], []

    if not isinstance(data, dict):
        return [], []

    return _clean_followups(data.get("followups")), _clean_links(data.get("links"))


__all__ = ["parse_extras"]
