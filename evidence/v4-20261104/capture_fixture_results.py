from pathlib import Path
import sys, json, datetime, subprocess
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "tests"))
from test_selected_candidate import run
from test_publish_quality_review import ReviewClient, REWRITE

cases = {}
for label, client in [
    ("A87-B93", ReviewClient(first_score=87, second_score=93)),
    ("A92", ReviewClient(first_score=92)),
    ("unsafe-B", ReviewClient(first_score=87, rewrite=REWRITE + " It improves results by 42%.")),
    ("low-B", ReviewClient(first_score=87, second_score=87)),
]:
    result, calls = run(client)
    cases[label] = {
        "mode": "fixture", "result": result.model_dump(),
        "visual_inputs": calls, "visual_call_count": len(calls),
        "quality_call_count": client.quality_calls,
        "rewrite_call_count": sum("one bounded publish-quality rewrite" in c["system"] for c in client.calls),
        "total_llm_fixture_calls": len(client.calls),
    }
record = {
    "head_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": ".venv/bin/python evidence/v4-20261104/capture_fixture_results.py",
    "mode": "fixture", "cases": cases,
}
Path("evidence/v4-20261104/P1-candidate-observations.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({k: {"selected": v["result"]["selected_candidate"], "visual_calls": v["visual_call_count"], "rewrite_calls": v["rewrite_call_count"]} for k, v in cases.items()}))
