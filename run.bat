@echo off
echo Starting URL Collector Application...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Run the Flask application
python app.py

REM If there's an error, pause
if %ERRORLEVEL% NEQ 0 (
    echo Application exited with an error.
    pause
)
