from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
REGISTRY = CONFIG_DIR / "calendar_registry.json"
RULES_YAML = CONFIG_DIR / "normalization_rules.yaml"

REQUIRED_ALWAYS = {"topic"}
CALENDAR_HINTS = {"service", "pillar", "audience", "date"}
FORCE_INCLUDE_FILE_HINTS = ["schedule", "calendar", "linkedin", "ardent", "20week", "graham"]

SYNONYMS = {
    "topic": [
        "topic",
        "topics",
        "title",
        "subject",
        "post",
        "theme",
        "headline",
        "hook theme",
        "hook",
        "content theme",
    ],
    "service": [
        "service",
        "services",
        "offering",
        "offerings",
        "product",
        "practice",
        "service tie-in",
        "service tie in",
        "service tie",
        "service mapping",
        "ardent service tie-in",
        "ardent service tie in",
    ],
    "pillar": ["pillar", "content pillar", "content_pillar"],
    "audience": ["audience", "target", "persona", "buyer", "industry focus", "industry"],
    "date": ["date", "day", "publish date", "post date"],
}

CANON_ORDER = ["date", "topic", "service", "pillar", "audience"]


def _read_csv_robust(path: Path, nrows: int | None = None) -> pd.DataFrame:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        for engine in ("c", "python"):
            try:
                return pd.read_csv(path, nrows=nrows, encoding=enc, engine=engine)
            except Exception:
                continue
    return pd.read_csv(path, nrows=nrows)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore

        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _dump_yaml(path: Path, data: dict[str, Any]) -> None:
    try:
        import yaml  # type: ignore

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    except Exception:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_normalization_rules() -> dict[str, Any]:
    return _load_yaml(RULES_YAML)


def save_normalization_rules(rules: dict[str, Any]) -> None:
    _dump_yaml(RULES_YAML, rules)


def _canonical_name(name: str, extra_synonyms: dict[str, list[str]] | None = None) -> str:
    low = name.lower().strip()
    low = re.sub(r"\s+", " ", low)
    syn = dict(SYNONYMS)
    if extra_synonyms:
        for k, v in extra_synonyms.items():
            syn.setdefault(k, [])
            for alias in v:
                if alias not in syn[k]:
                    syn[k].append(alias)
    for canon, alts in syn.items():
        for a in alts:
            if low == a or low.startswith(a):
                return canon
    return low


def _coalesce(df: pd.DataFrame, cols: list[str], new_name: str) -> pd.DataFrame:
    if not cols:
        return df
    series = None
    for c in cols:
        s = df[c]
        if series is None:
            series = s
        else:
            series = series.where(series.notna() & (series.astype(str).str.strip() != ""), s)
    df = df.drop(columns=cols, errors="ignore")
    df[new_name] = series
    return df


def _normalize_columns(
    df: pd.DataFrame, file_name: str, rules: dict[str, Any]
) -> tuple[pd.DataFrame, dict[str, str]]:
    extra_synonyms = rules.get("global_synonyms", {})
    file_overrides = rules.get("files", {}).get(file_name, {})
    col_aliases = file_overrides.get("column_aliases", {})  # exact column -> canonical name

    mapping: dict[str, str] = {}
    for c in df.columns:
        canon = _canonical_name(str(c), extra_synonyms)
        mapping[c] = canon

    # Apply explicit column_aliases first (exact, case-insensitive match)
    for orig, target in list(col_aliases.items()):
        for real in df.columns:
            if str(real).strip().lower() == str(orig).strip().lower():
                mapping[real] = target.strip().lower()

    expose: dict[str, str] = {}
    for c, canon in mapping.items():
        if canon in {"date", "topic", "pillar", "service", "audience"}:
            expose[c] = canon

    # Backup loose prefix
    for want in ["date", "pillar", "audience"]:
        if want not in expose.values():
            for c in df.columns:
                if str(c).strip().lower().startswith(want):
                    expose[c] = want
                    break

    df2 = df.rename(columns=expose)

    # Dedupe canonical columns by coalescing
    for key in CANON_ORDER:
        dupes = [c for c in df2.columns if c == key]
        if len(dupes) > 1:
            tmp_names = []
            for i, col in enumerate(dupes):
                new_col = f"__{key}_{i}"
                df2.rename(columns={col: new_col}, inplace=True)
                tmp_names.append(new_col)
            df2 = _coalesce(df2, tmp_names, key)

    # If service missing but service-like column exists
    if "service" not in df2.columns:
        for c in df.columns:
            lc = str(c).lower()
            if "service" in lc and (
                "tie" in lc or "offering" in lc or "practice" in lc or "product" in lc
            ):
                df2["service"] = df[c]
                break

    return df2, expose


def _best_topic(raw: pd.DataFrame, normalized: pd.DataFrame) -> pd.Series | None:
    candidates = []

    def score(s: pd.Series) -> int:
        try:
            return int((s.astype(str).str.strip() != "").sum())
        except Exception:
            return 0

    # normalized
    if "topic" in normalized.columns:
        candidates.append(("normalized.topic", normalized["topic"], score(normalized["topic"])))
    # raw topic-like
    topic_aliases = set(SYNONYMS["topic"] + ["topic"])
    for c in raw.columns:
        lc = str(c).lower().strip()
        if lc in topic_aliases or any(lc.startswith(a) for a in topic_aliases):
            s = raw[c]
            candidates.append((f"raw.{c}", s, score(s)))
    if not candidates:
        return None
    best = max(candidates, key=lambda x: x[2])
    s = best[1]
    try:
        s = s.astype(str).str.strip().replace({"nan": "", "None": ""})
    except Exception:
        pass
    return s


def normalize_calendar(df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    rules = load_normalization_rules()
    df2, _ = _normalize_columns(df, file_name, rules)

    # Build/repair topic
    topic_series = _best_topic(df, df2)
    if topic_series is not None:
        df2["topic"] = topic_series

    # Trim
    for c in df2.columns:
        if pd.api.types.is_object_dtype(df2[c]):
            df2[c] = df2[c].astype(str).str.strip().replace({"nan": "", "None": ""})

    # Ensure canonical columns
    for c in CANON_ORDER:
        if c not in df2.columns:
            df2[c] = ""

    # Drop empty topics
    df2["topic"] = df2["topic"].astype(str).str.strip()
    df2 = df2[df2["topic"] != ""]

    # Dates
    if "date" in df2.columns:
        try:
            dt = pd.to_datetime(df2["date"], errors="coerce")
            iso = dt.dt.strftime("%Y-%m-%d")
            df2.loc[dt.notna(), "date"] = iso[dt.notna()]
        except Exception:
            pass

    # Reorder
    present = [c for c in CANON_ORDER if c in df2.columns]
    others = [c for c in df2.columns if c not in present]
    df2 = df2[present + others]

    # Dedup
    try:
        if "date" in df2.columns:
            df2 = df2.drop_duplicates(subset=["date", "topic"], keep="first")
        else:
            df2 = df2.drop_duplicates(subset=["topic"], keep="first")
    except Exception:
        pass

    return df2.reset_index(drop=True)


def _read_registry() -> dict[str, str]:
    if REGISTRY.exists():
        try:
            return json.loads(REGISTRY.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _write_registry(m: dict[str, str]) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(m, indent=2), encoding="utf-8")


def get_registry() -> dict[str, str]:
    return _read_registry()


def upsert_registry(file_name: str, display_name: str) -> None:
    reg = _read_registry()
    reg[file_name] = display_name
    _write_registry(reg)


def display_name_for(file_name: str) -> str:
    reg = _read_registry()
    return reg.get(file_name, file_name)


def list_personas(personas_yaml: dict[str, Any]) -> list[str]:
    personas = personas_yaml.get("personas", {}) if isinstance(personas_yaml, dict) else {}
    return list(personas.keys()) or ["ardent_v2"]


def discover_with_reasons() -> tuple[list[str], dict[str, str]]:
    valid: list[str] = []
    invalid: dict[str, str] = {}
    for p in DATA_DIR.glob("*.csv"):
        try:
            raw = _read_csv_robust(p, nrows=None)
            norm = normalize_calendar(raw.copy(), p.name)
            if "topic" in norm.columns and len(norm) > 0:
                valid.append(p.name)
            else:
                pieces = []
                if "topic" not in norm.columns:
                    pieces.append("No 'topic' column after normalization.")
                if len(norm) == 0:
                    pieces.append("No rows with non-empty topics after normalization.")
                pieces.append(f"Raw columns: {list(raw.columns)}")
                invalid[p.name] = " ".join(pieces)
        except Exception as e:
            invalid[p.name] = f"Error reading/normalizing: {e}"
    return sorted(sorted(set(valid))), invalid


def discover_calendars() -> list[str]:
    valid, _ = discover_with_reasons()
    return valid


def df_to_markdown_row(row: dict[str, Any]) -> str:
    date = str(row.get("date", "")).split(" ")[0] if row.get("date") else ""
    weekday = ""
    try:
        if date:
            weekday = pd.to_datetime(date, errors="coerce").day_name()
    except Exception:
        weekday = ""
    date_disp = f"{date} ({weekday})" if date and weekday else date
    line1 = (
        f"**{date_disp} — {row.get('topic','')}**" if date_disp else f"**{row.get('topic','')}**"
    )
    meta = " • ".join(
        [x for x in [row.get("pillar", ""), row.get("service", ""), row.get("audience", "")] if x]
    )
    return f"{line1}\n{meta}"
