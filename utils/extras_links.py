from __future__ import annotations

import re
from typing import Any

from llm.knowledge import CONTENT

_URL_RE = re.compile(r"https?://[^\s<>\"')]+")


def _normalize_url(url: str) -> str:
    url = url.strip().rstrip(".,;:")
    if url.startswith("http://"):
        url = "https://" + url[len("http://") :]
    return url.rstrip("/")


ALLOWED_URLS = {
    _normalize_url(match)
    for text in CONTENT.values()
    for match in _URL_RE.findall(text)
}
ALLOWED_URLS.add("mailto:negiritik01@gmail.com")


def _is_allowed(url: str) -> bool:
    if url.lower().startswith("mailto:"):
        return url.lower() == "mailto:negiritik01@gmail.com"
    return _normalize_url(url) in ALLOWED_URLS


def _clean_links(value: Any) -> list[dict[str, str]]:
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        return []

    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in value:
        label = ""
        url = ""

        if isinstance(item, dict):
            label = str(item.get("label") or item.get("title") or "").strip()
            url = str(item.get("url") or item.get("href") or "").strip()
        elif isinstance(item, str):
            match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", item.strip())
            if match:
                label, url = match.group(1), match.group(2)
            elif "|" in item:
                label, url = [part.strip() for part in item.split("|", 1)]
            else:
                url = item.strip()

        if not url or not _is_allowed(url):
            continue

        if url.lower().startswith("mailto:"):
            url = "mailto:negiritik01@gmail.com"
        else:
            url = _normalize_url(url)

        label = " ".join(label.split())[:60] or url
        key = _normalize_url(url)
        if key in seen:
            continue
        seen.add(key)
        out.append({"label": label, "url": url})
        if len(out) >= 3:
            break
    return out


__all__ = ["ALLOWED_URLS", "_clean_links", "_is_allowed", "_normalize_url"]
