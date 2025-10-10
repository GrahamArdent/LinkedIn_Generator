# Copilot guide (repo context)

Give Copilot enough context and constraints so it helps, not hurts.

## General prompt pattern
> You are contributing to a Streamlit app with CSV normalization utilities.  
> Follow our standards in `pyproject.toml` and `ui/utils.py`.  
> Do not change public function signatures without tests.  
> Output patch-style diffs or new files; keep PRs small.

## Common tasks
- **Adjust normalization**: Edit `ui/utils.py` → `SYNONYMS` or `normalize_calendar()`.
- **Add column mapping** for a new file: Update `config/normalization_rules.yaml` under `files: <file>.csv: column_aliases:`
- **Write tests**: Add cases in `tests/test_normalize.py` for new headers or edge-cases.
- **UI tweaks**: Modify `ui/app.py` (keep `width='stretch'`).

## Review checklist for Copilot PRs
- ruff + black pass
- tests updated/added
- docs updated if behavior changes
