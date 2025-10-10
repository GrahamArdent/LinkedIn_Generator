@echo off
REM Run today's scheduled post and save files to out\
SETLOCAL
cd /d "C:\PYTHON APPS\LinkedIn_Generator"
call ".\.venv\Scripts\activate"
cd /d "C:\PYTHON APPS\LinkedIn_Generator\src"
python -m app.cli post
ENDLOCAL
