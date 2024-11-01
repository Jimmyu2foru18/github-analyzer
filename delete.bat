@echo off
echo Cleaning up project structure...
echo ===========================

:: Remove all src directory and contents
echo Removing src directory and contents...
if exist "src" (
    rmdir /s /q "src"
    echo Removed src directory
)

:: Remove unnecessary batch file
echo Removing unnecessary files...
if exist "run_project.bat" (
    del "run_project.bat"
    echo Removed run_project.bat
)

:: Remove pyvenv.cfg (will be regenerated)
if exist "venv\pyvenv.cfg" (
    del "venv\pyvenv.cfg"
    echo Removed pyvenv.cfg
)

echo.
echo Cleanup complete!
echo ================
echo.
echo Remaining project files:
dir /b *.py *.bat *.txt *.yaml *.cfg 2>nul

pause 