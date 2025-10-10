@echo off
setlocal
cd /d %~dp0
set PYTHONPATH=%CD%
echo Starting Streamlit with PYTHONPATH=%PYTHONPATH%
streamlit run ui\app.py
