@echo off
cd /d "%~dp0..\backend"
if not exist "..\data" mkdir "..\data"
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
