# LinkedIn_Generator

Minimal Streamlit app + utilities to generate LinkedIn posts from calendar CSVs.  
This repo includes:
- Robust CSV **normalization** (maps different headers to `date, topic, service, pillar, audience`)
- A minimal **Streamlit UI**
- A CLI **converter** to normalize any CSV
- GitHub **CI** (ruff, black, pytest) and optional **CodeQL**
- Pre-commit hooks and Copilot guide

## Quick start

```bash
# 1) Create and activate a venv (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2) Install
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional (dev tools)

# 3) Run the app
streamlit run ui/app.py
```

Drop your calendar CSVs in `data/`. Use the **Manual Column Mapper** in the sidebar if a file is ignored.

## CLI converter

```bash
python scripts/convert_calendar.py data/your_calendar.csv
# -> normalized_your_calendar.csv
```

## Tests

```bash
pytest -q
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For Copilot prompts and conventions see [docs/COPILOT_GUIDE.md](docs/COPILOT_GUIDE.md).
