@echo off
REM Alcohol Mechanism Batch Extraction Launcher
REM This script helps you set up and run the extraction pipeline

echo ================================================================================
echo ALCOHOL MECHANISM BATCH EXTRACTION
echo ================================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ and try again
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if ANTHROPIC_API_KEY is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo WARNING: ANTHROPIC_API_KEY environment variable is not set
    echo.
    echo You need to set your Anthropic API key to run this extraction.
    echo.
    echo Option 1: Set it for this session only:
    echo   set ANTHROPIC_API_KEY=your-key-here
    echo   start_extraction.bat
    echo.
    echo Option 2: Set it permanently:
    echo   setx ANTHROPIC_API_KEY "your-key-here"
    echo   Then restart this script
    echo.
    set /p API_KEY="Enter your Anthropic API key now (or press Enter to exit): "

    if "%API_KEY%"=="" (
        echo Cancelled.
        pause
        exit /b 1
    )

    set ANTHROPIC_API_KEY=%API_KEY%
    echo.
    echo API key set for this session.
    echo.
)

echo API Key: %ANTHROPIC_API_KEY:~0,10%...
echo.

REM Show menu
echo What would you like to do?
echo.
echo [1] Test extraction (single query, validates pipeline)
echo [2] Run Phase 1 only (Direct health consequences, ~15-20 mechanisms)
echo [3] Run Phases 1-3 (Health + Risk + Social, ~45-50 mechanisms)
echo [4] Run ALL phases (Complete extraction, ~90-130 mechanisms, 3-6 hours, $50-100)
echo [5] Run in TEST mode (2 queries per phase, validates all phases)
echo [0] Exit
echo.

set /p CHOICE="Enter your choice (0-5): "

if "%CHOICE%"=="0" (
    echo Cancelled.
    exit /b 0
)

if "%CHOICE%"=="1" (
    echo.
    echo Running test extraction...
    echo.
    cd backend
    python scripts/test_extraction.py
    goto end
)

if "%CHOICE%"=="2" (
    echo.
    echo Running Phase 1 (Direct Health Consequences)...
    echo This will take approximately 30-60 minutes
    echo Cost: ~$10-15
    echo.
    set /p CONFIRM="Proceed? (y/n): "
    if /i not "%CONFIRM%"=="y" goto cancelled
    cd backend
    python scripts/run_alcohol_extraction.py --phases 1 --limit 10
    goto end
)

if "%CHOICE%"=="3" (
    echo.
    echo Running Phases 1-3...
    echo This will take approximately 1-2 hours
    echo Cost: ~$25-35
    echo.
    set /p CONFIRM="Proceed? (y/n): "
    if /i not "%CONFIRM%"=="y" goto cancelled
    cd backend
    python scripts/run_alcohol_extraction.py --phases 1 2 3 --limit 10
    goto end
)

if "%CHOICE%"=="4" (
    echo.
    echo WARNING: Full extraction will:
    echo - Run all 6 phases (90 queries)
    echo - Retrieve 300-500 papers
    echo - Extract 90-130 mechanisms
    echo - Take 3-6 hours
    echo - Cost $50-100 in API credits
    echo.
    set /p CONFIRM="Are you sure? (yes/no): "
    if /i not "%CONFIRM%"=="yes" goto cancelled
    cd backend
    python scripts/batch_alcohol_mechanisms.py
    goto end
)

if "%CHOICE%"=="5" (
    echo.
    echo Running TEST mode (2 queries per phase)...
    echo This will validate all phases with minimal cost (~$5-10)
    echo.
    set /p CONFIRM="Proceed? (y/n): "
    if /i not "%CONFIRM%"=="y" goto cancelled
    cd backend
    python scripts/run_alcohol_extraction.py --test --phases 1 2 3 4 5 6
    goto end
)

echo Invalid choice.
goto end

:cancelled
echo.
echo Cancelled.
goto end

:end
echo.
echo ================================================================================
echo.
echo Next steps:
echo 1. Validate mechanisms: python mechanism-bank/validation/validate_mechanisms.py
echo 2. Review extracted mechanisms in mechanism-bank/mechanisms/
echo 3. Load to database: curl -X POST http://localhost:8000/api/mechanisms/admin/load-from-yaml
echo 4. Commit to git
echo.
echo See backend/scripts/README_ALCOHOL_EXTRACTION.md for full guide
echo.
echo ================================================================================
pause
