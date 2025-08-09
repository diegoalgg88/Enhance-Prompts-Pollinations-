@echo off
REM Check for administrative privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd.exe -ArgumentList '/c %~s0' -Verb RunAs"
    exit
)

REM Get the directory of the batch file
set "BATCH_DIR=%~dp0"

REM Set the path to the virtual environment's Python executable
set "PYTHON_EXE=%BATCH_DIR%.venv\Scripts\python.exe"
set "SCRIPT_PATH=%BATCH_DIR%project\main.py"

REM Check if the Python executable exists
if not exist "%PYTHON_EXE%" (
    echo Python executable not found in .venv.
    echo Please run setup.py first to create the virtual environment and install dependencies.
    pause
    exit
)

REM Run the main script
echo Starting the application...
"%PYTHON_EXE%" "%SCRIPT_PATH%"

pause
