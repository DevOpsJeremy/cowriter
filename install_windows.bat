@echo off
echo Installing Cowriter...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found, proceeding with installation...

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python main.py
echo.
echo Or install as a package:
echo   python -m pip install -e .
echo   cowriter
echo.
pause
