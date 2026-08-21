@echo off
cd /d "%~dp0..\frontend"
if not exist "node_modules" (
  echo Missing frontend dependencies.
  echo Run first:
  echo   cd frontend
  echo   npm install
  pause
  exit /b 1
)
npm run dev
