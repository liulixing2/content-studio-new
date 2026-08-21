@echo off
cd /d "%~dp0..\backend"
if not exist ".venv\Scripts\python.exe" (
  echo Missing backend virtual environment.
  echo Create it first with:
  echo   python -m venv backend\.venv
  echo   backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
  pause
  exit /b 1
)
".venv\Scripts\python.exe" manage.py migrate
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
