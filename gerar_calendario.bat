@echo off
python "%~dp0scripts\build_calendar.py"
timeout /t 3 /nobreak >nul
