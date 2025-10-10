from __future__ import annotations
import csv, os, re
from typing import List, Dict, Any
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def read_whitelist() -> List[str]:
    wl = DATA_DIR / "source_whitelist.txt"
    if wl.exists():
        return [ln.strip().lower() for ln in wl.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return []

def load_citations() -> List[Dict[str,Any]]:
    path = DATA_DIR / "citations.csv"
    rows: List[Dict[str,Any]] = []
    if not path.exists():
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = {k:(v or "").strip() for k,v in row.items()}
            row["whitelist"] = str(row.get("whitelist","")).lower() in ("true","1","yes")
            rows.append(row)
    return rows

def lexical_score(s: str, q: str) -> int:
    s = s.lower()
    score = 0
    for w in re.findall(r"[a-z0-9]{3,}", q.lower()):
        if w in s:
            score += 1
    return score

def retrieve(topic:str, angle:str, k:int=3) -> List[Dict[str,Any]]:
    wl = read_whitelist()
    items = load_citations()
    scored = []
    query = f"{topic} {angle}".strip()
    for it in items:
        base = f"{it.get('title','')} {it.get('one_liner','')} {it.get('tags','')} {it.get('domain','')}"
        score = lexical_score(base, query)
        dom = (it.get("domain","") or "").lower()
        if wl and dom and dom not in wl and not it.get("whitelist"):
            score -= 2
        scored.append((score, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for sc,it in scored[:max(1,k)] if sc >= 0]
