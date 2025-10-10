# Windows scheduling (1–2 minutes)

## One‑time check
- Confirm your venv exists: `C:\PYTHON APPS\LinkedIn_Generator\.venv\Scripts\python.exe`

## Option A — Quick manual run any time
Double‑click: `scripts\run_post_today.bat`  
This activates the venv and runs `python -m app.cli post`.

## Option B — Daily automatic run (Task Scheduler)
1. Press Start, search **Task Scheduler** → open.
2. Right panel → **Create Basic Task…**
3. Name: `LinkedIn Daily Post`
4. Trigger: **Daily** → Next → Start time = the `time_of_day_local` in `config\schedule.yaml` (e.g., 9:15 AM).
5. Action: **Start a program** → Program/script:
   ```
   C:\Windows\System32\cmd.exe
   ```
   Add arguments:
   ```
   /c "C:\PYTHON APPS\LinkedIn_Generator\scripts\run_post_today.bat"
   ```
   Start in:
   ```
   C:\PYTHON APPS\LinkedIn_Generator
   ```
6. Finish.

### Verify who posts on a future date
From project root in a Command Prompt (venv not required):
```
python scripts\which_persona.py 2025-10-13
```
It prints `graham` or `ardent` based on `config\schedule.yaml`.

> The app itself decides the persona for today using the same file.
