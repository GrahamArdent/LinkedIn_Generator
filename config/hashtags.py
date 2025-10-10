from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional
import re
import yaml
from collections import Counter

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9\-]+")

DEFAULT_POLICY = {
    "min_per_post": 3,
    "max_per_post": 5,
    "core": ["#CyberSecurity"],
    "brand": ["#ArdentSecurity"],
    "banlist": ["#Security"],
    "keyword_map": {},
    "trending_priority": [],
}

STOPWORDS = {
    "the","a","an","and","or","but","of","for","with","on","in","to","from","by",
    "is","are","was","were","be","been","it","this","that","as","at","into","about",
    "we","you","our","their","they","i","me","my","your","yours","us","them","he","she",
}

def _load_yaml(path: Path) -> dict:
    if not path or not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}

def load_policy(config_dir: Path) -> Dict:
    policy_path = config_dir / "hashtag_policy.yaml"
    policy = DEFAULT_POLICY.copy()
    policy.update(_load_yaml(policy_path))
    # normalize lists
    for k in ("core","brand","banlist","trending_priority"):
        policy[k] = list(dict.fromkeys(policy.get(k, [])))  # de-dup preserve order
    return policy

def _camel_hashtag(tokens: List[str]) -> str:
    # join tokens into CamelCase hashtag
    parts = []
    for t in tokens:
        t = re.sub(r"[^A-Za-z0-9]", "", t)
        if not t:
            continue
        parts.append(t[:1].upper() + t[1:].lower())
    if not parts:
        return ""
    return "#" + "".join(parts)

def _extract_keywords(text: str, top_k: int = 12) -> List[str]:
    words = [w.lower() for w in WORD_RE.findall(text)]
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    counts = Counter(words)
    return [w for w, _ in counts.most_common(top_k)]

def _unique_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            out.append(x); seen.add(x)
    return out

def generate_hashtags(
    body_text: str,
    persona: str,
    topic: Optional[str],
    config_dir: Path,
) -> List[str]:
    """
    Heuristic, post-aware hashtag generator tuned for LinkedIn:
      - 3–5 tags
      - include 1 core tag (#CyberSecurity), 1–2 topical tags from body/topic
      - optional brand for 'ardent'
      - prefer trending when relevant
      - filter banlist & dedupe
    """
    policy = load_policy(config_dir)
    min_n = int(policy.get("min_per_post", 3))
    max_n = int(policy.get("max_per_post", 5))
    core = list(policy.get("core") or [])
    brand = list(policy.get("brand") or [])
    ban = set((policy.get("banlist") or []))
    kmap = {str(k).lower(): v for k, v in (policy.get("keyword_map") or {}).items()}
    trending = list(policy.get("trending_priority") or [])

    # keywords from body + topic
    kw = _extract_keywords((topic or "") + " " + (body_text or ""))
    topical: List[str] = []
    for w in kw:
        if w in kmap:
            topical.append(kmap[w])
        else:
            # build a neat tag from single word (fallback), skip very generic
            if w in ("security","cybersecurity","technology","company","people"):
                continue
            tag = _camel_hashtag([w])
            if len(tag) > 2:
                topical.append(tag)

    # prefer trending versions if present
    topical = _unique_keep_order(topical)
    # lightweight “trending lift”: move any trending tags that already exist to the front
    topical = _unique_keep_order([t for t in trending if t in topical] + topical)

    # seed list
    chosen: List[str] = []
    if core:
        chosen.append(core[0])  # keep one core anchor
    if persona == "ardent" and brand:
        chosen.append(brand[0])

    # fill with topical until max
    for t in topical:
        if len(chosen) >= max_n:
            break
        chosen.append(t)

    # post-filter
    chosen = [t for t in chosen if t and t not in ban]
    chosen = _unique_keep_order(chosen)

    # enforce bounds
    if len(chosen) < min_n:
        # backfill from remaining cores/trending
        pool = _unique_keep_order((core + trending + topical))
        for t in pool:
            if len(chosen) >= min_n:
                break
            if t not in chosen and t not in ban:
                chosen.append(t)

    return chosen[:max_n]

def ensure_hashtags_in_body(body: str, tags: List[str]) -> str:
    """
    Remove any trailing hashtag block and append our fresh set as the final line.
    """
    lines = body.rstrip().splitlines()
    # find last non-empty block that looks like hashtags
    i = len(lines) - 1
    while i >= 0 and (lines[i].strip().startswith("#") or lines[i].strip() == ""):
        i -= 1
    new = lines[: i + 1]
    if tags:
        new.append(" ".join(tags))
    return "\n".join(new).strip()
