@echo off
REM Simple batch file to pull code and run tests

echo Updating code from GitHub...
git pull

REM Continue execution regardless of git pull result
if %errorlevel% neq 0 (
    echo Git pull failed, but continuing with test execution...
) else (
    echo Git pull successful
)

echo Running tests...
".venv\Scripts\python.exe" run_tests.py

if %errorlevel% neq 0 (
    echo Test run failed
    pause
    exit /b %errorlevel%
)

echo Test run completed!
pause