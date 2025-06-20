@echo off
echo 🚀 Starting Monk-AI Multi-Agent System...

echo Stopping existing servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul

echo Starting FastAPI backend server...
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload --port 8000"

echo Waiting for backend to start...
timeout /t 5 >nul

echo Starting React frontend server...
cd frontend
start "Frontend Server" cmd /k "npm start"
cd ..

echo ✅ Both servers are starting up!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Multi-Agent Orchestrator: http://localhost:3000/multi-agent
echo.
echo Press any key to continue...
pause >nul 