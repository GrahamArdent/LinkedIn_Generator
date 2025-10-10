from __future__ import annotations
import re
from typing import Dict, Any

LINK_RE = re.compile(r"https?://\S+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")
EM_DASH = "—"

def judge_score(text:str, persona:Dict[str,Any], rules:Dict[str,Any]) -> int:
    score = 100
    w = len(text.split())
    score -= abs(w - 190) // 2
    score -= 15 if LINK_RE.search(text) else 0
    score -= 10 * max(0, len(EMOJI_RE.findall(text)) - int(rules.get("emoji_max",3)))
    if EM_DASH in text and not rules.get("allow_em_dash", False):
        score -= 10
    if "short_paragraphs" in persona.get("rhythm", []):
        paras = [p.strip() for p in text.split("\n") if p.strip()]
        if any(len(p.split()) > 120 for p in paras):
            score -= 10
    return max(0, min(100, score))
