@echo off
setlocal
cd /d "%~dp0.."
set DB_FILE=data\content_studio.sqlite3

echo This will delete local test data only:
echo   %CD%\%DB_FILE%
echo.
echo It will not touch source code, Git history, or the legacy project.
echo Type RESET to continue, or close this window to cancel.
set /p CONFIRM=Confirm: 

if /I not "%CONFIRM%"=="RESET" (
  echo Cancelled.
  pause
  exit /b 0
)

if exist "%DB_FILE%" (
  del "%DB_FILE%"
  echo Local database deleted.
) else (
  echo Local database does not exist.
)

echo Run scripts\start_backend.bat next. It will recreate the database.
pause
