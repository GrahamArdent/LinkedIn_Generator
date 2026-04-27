#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Bootstrap sys.path so 'ui' imports work regardless of CWD
BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from ui.utils import _read_csv_robust, normalize_calendar  # noqa: E402


def resolve_input_path(arg: str) -> Path:
    p = Path(arg)
    # If they passed without extension, assume .csv
    if p.suffix.lower() != ".csv":
        p_csv = p.with_suffix(".csv")
    else:
        p_csv = p
    # Try as-is
    if p_csv.exists():
        return p_csv
    # Try relative to project /data
    candidate = BASE / "data" / p_csv.name
    if candidate.exists():
        return candidate
    # Try the original (maybe with different suffix they want pandas to infer)
    if p.exists():
        return p
    raise FileNotFoundError(f"Could not find input file: {arg}. Tried: {p_csv}, {candidate}")


def main():
    ap = argparse.ArgumentParser(
        description="Normalize a calendar CSV into canonical columns (date, topic, service, pillar, audience)."
    )
    ap.add_argument("input", help="Path or filename of input CSV (extension optional).")
    ap.add_argument(
        "-o",
        "--output",
        help="Path to write normalized CSV (default: alongside input with prefix 'normalized_')",
    )
    args = ap.parse_args()

    inp = resolve_input_path(args.input)
    out = Path(args.output) if args.output else inp.with_name(f"normalized_{inp.name}")
    df = _read_csv_robust(inp)
    norm = normalize_calendar(df, inp.name)
    # Ensure stable column order
    cols = [c for c in ["date", "topic", "service", "pillar", "audience"] if c in norm.columns] + [
        c for c in norm.columns if c not in ["date", "topic", "service", "pillar", "audience"]
    ]
    norm = norm[cols]
    norm.to_csv(out, index=False, encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
