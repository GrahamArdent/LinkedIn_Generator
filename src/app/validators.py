from __future__ import annotations

import re

LINK_RE = re.compile(r"https?://\S+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")


def remove_links(text: str) -> tuple[str, list[str]]:
    urls = LINK_RE.findall(text)
    clean = LINK_RE.sub("", text)
    return clean.strip(), urls


def append_sources_block(body: str, urls: list[str]) -> str:
    if not urls:
        return body.rstrip()
    return f"{body.rstrip()}\n\nSources:\n" + "\n".join(urls)


def normalize_bullets(text: str, bullet: str = "🔹") -> str:
    return re.sub(r"(?m)^[ \t]*[-•][ \t]+", f"{bullet} ", text)


def cap_emojis(text: str, max_n: int = 3) -> str:
    emojis = EMOJI_RE.findall(text)
    if len(emojis) <= max_n:
        return text
    for extra in emojis[max_n:]:
        text = text.replace(extra, "", 1)
    return text


def replace_em_dashes(text: str) -> str:
    return text.replace("—", " - ")


def clamp_hashtags(hashtags: list[str], min_n: int = 3, max_n: int = 5) -> list[str]:
    unique = []
    seen = set()
    for h in hashtags:
        if not h.startswith("#"):
            h = "#" + h.lstrip("#")
        lower = h.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(h)
    if len(unique) < min_n:
        return unique
    return unique[:max_n]


def extract_hashtags(text: str) -> list[str]:
    return HASHTAG_RE.findall(text)


def _normalize_spacing(text: str) -> str:
    lines = [re.sub(r"[ \t]{2,}", " ", line).rstrip() for line in text.splitlines()]
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def apply_house_rules(body: str, *, bullet="🔹", emoji_max: int = 3, allow_em_dash: bool = False):
    issues: list[str] = []
    b1 = normalize_bullets(body, bullet=bullet)
    b2 = cap_emojis(b1, max_n=emoji_max)
    b3 = b2 if allow_em_dash else replace_em_dashes(b2)
    b3 = _normalize_spacing(b3)
    return b3, issues
