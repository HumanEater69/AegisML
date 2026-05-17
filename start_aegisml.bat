@echo off
echo ==================================================
echo      AEGISML ENTERPRISE - PLATFORM LAUNCHER
echo ==================================================
echo.
echo [1/3] Verifying dependencies...
pip install -r requirements.txt >nul 2>&1

echo [2/3] Initializing Quantum Inference API (Backend)...
:: Kill existing process on port 8080 to prevent conflicts
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
start "AegisML Quantum API" cmd /k "title AegisML Backend & set PYTHONPATH=%cd% & echo Starting FastAPI Server on Port 8080... & python -m uvicorn src.inference.main:app --host 0.0.0.0 --port 8080"

:: Wait for 4 seconds to let the API start fully
timeout /t 4 /nobreak >nul

echo [3/3] Booting Liquid Glass UI (Frontend)...
title AegisML Dashboard
set PYTHONPATH=%cd%
streamlit run dashboard/app.py
