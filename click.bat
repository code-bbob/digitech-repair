@echo off
cd /d D:\digitech-repair\backend
start python manage.py runserver

:WAITLOOP
timeout /t 1 /nobreak >nul
netstat -aon | findstr :8000 | findstr LISTENING >nul
if errorlevel 1 goto WAITLOOP

start chrome http://127.0.0.1:8000/
