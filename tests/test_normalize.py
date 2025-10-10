from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.utils import normalize_calendar  # noqa: E402

def test_normalize_maps_common_headers():
    df = pd.DataFrame({
        "Date": ["2025-01-05", ""],
        "Hook Theme": ["Topic A", ""],
        "Ardent Service Tie-In": ["Service X", ""],
        "Content Pillar": ["Pillar Y", ""],
        "Industry Focus": ["Audience Z", ""],
    })
    out = normalize_calendar(df, "dummy.csv")
    assert list(out.columns)[:5] == ["date","topic","service","pillar","audience"]
    assert out.shape[0] == 1
    assert out.loc[0, "topic"] == "Topic A"
    assert out.loc[0, "service"] == "Service X"

def test_normalize_parses_dates():
    df = pd.DataFrame({
        "Date": ["10/05/2025", "2025-10-06"],
        "Topic": ["A","B"],
    })
    out = normalize_calendar(df, "dummy.csv")
    # One of EU/US date interpretations is OK for first row
    assert out.loc[1, "date"] == "2025-10-06"
