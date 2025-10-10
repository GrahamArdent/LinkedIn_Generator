@echo off
REM Launch the Streamlit UI
cd /d "C:\PYTHON APPS\LinkedIn_Generator"
call ".\.venv\Scripts\activate"
streamlit run ui\streamlit_app.py
