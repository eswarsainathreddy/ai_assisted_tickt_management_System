@echo off
echo =========================================================
echo Starting Agentic AI Ticket Resolution System
echo Backend: Connected to Neon PostgreSQL (Port 8000)
echo Frontend: Streamlit Dashboard (Port 8501)
echo =========================================================

start "FastAPI Backend (Neon DB)" cmd /k "python -m uvicorn src.main:app --port 8000"

echo Waiting for backend to connect to Neon...
timeout /t 6 /nobreak >nul

start "Streamlit Frontend" cmd /k "python -m streamlit run app.py"

echo System is running!
pause
