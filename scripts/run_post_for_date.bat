@echo off
REM Usage: run_post_for_date.bat YYYY-MM-DD [text|doc_carousel]
SETLOCAL
if "%~1"=="" (
  echo Usage: scripts\run_post_for_date.bat YYYY-MM-DD [text^|doc_carousel]
  EXIT /B 1
)
set POST_TYPE=%2
if "%POST_TYPE%"=="" set POST_TYPE=text
cd /d "C:\PYTHON APPS\LinkedIn_Generator"
call ".\.venv\Scripts\activate"
cd /d "C:\PYTHON APPS\LinkedIn_Generator\src"
python -m app.cli post --date %1 --post-type %POST_TYPE%
ENDLOCAL
