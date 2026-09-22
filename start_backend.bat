@echo off
echo ===================================================
echo Starting FastAPI Backend (Connected to Neon DB)...
echo ===================================================
python -m uvicorn src.main:app --port 8000
pause
