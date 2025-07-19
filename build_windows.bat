@echo off
echo Building Cowriter for Windows (Local Development)...
echo Note: For CI/CD builds, use GitHub Actions workflow
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Installing build dependencies...
python -m pip install pyinstaller

echo.
echo Installing project dependencies...
python -m pip install -r requirements.txt

echo.
echo Building executable...

REM Check if icon exists
if exist "src\assets\icon.ico" (
    echo Using custom icon...
    pyinstaller --windowed --onefile --name Cowriter --icon=src\assets\icon.ico src\__main__.py
) else (
    echo No icon found, building without icon...
    pyinstaller --windowed --onefile --name Cowriter src\__main__.py
)

if %errorlevel% neq 0 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Build complete!
echo Executable created in dist\Cowriter.exe
echo.

REM Clean up build files
echo Cleaning up build files...
rmdir /s /q build >nul 2>&1
del __main__.spec >nul 2>&1

echo.
echo Distribution ready: dist\Cowriter.exe
echo File size:
dir dist\Cowriter.exe | find "Cowriter.exe"
echo.
echo For automated builds and releases, push to GitHub and use Actions workflow
pause
