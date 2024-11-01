@echo off
echo GitHub Repository Analyzer and Builder (Development Mode)
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Activate virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
if errorlevel 1 (
    echo Error activating virtual environment!
    pause
    exit /b 1
)

:: Install/upgrade requirements
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo Error installing requirements!
    pause
    exit /b 1
)

:: Check for environment variables
if not defined GITHUB_TOKEN (
    echo WARNING: GITHUB_TOKEN environment variable is not set
    set /p GITHUB_TOKEN="Enter your GitHub token: "
    set "GITHUB_TOKEN=%GITHUB_TOKEN%"
)

if not defined OPENAI_API_KEY (
    echo WARNING: OPENAI_API_KEY environment variable is not set
    set /p OPENAI_API_KEY="Enter your OpenAI API key: "
    set "OPENAI_API_KEY=%OPENAI_API_KEY%"
)

:: Run with debug logging
echo.
echo Starting GitHub Repository Analyzer...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo An error occurred while running the project.
    echo Check the logs directory for details.
    pause
)

deactivate