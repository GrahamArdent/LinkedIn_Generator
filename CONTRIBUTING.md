# Contributing

- Use feature branches; open PRs to `main`.
- Run formatters and tests locally before pushing:
  ```bash
  ruff check .
  black --check .
  pytest -q
  ```
- Follow Conventional Commits: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```
