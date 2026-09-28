@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo   Pushing JARVIS MARK-XXXIX to GitHub...
echo ============================================================
echo.

git branch -M main
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Repository pushed to GitHub successfully!
    echo View it at: https://github.com/shaheerkhan0012345-dotcom/Jarvis
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo [NOTE] If the push failed with "Repository not found":
    echo 1. Go to https://github.com/new and create a new repository
    echo    named: Mark-XXXIX-OR
    echo 2. Run this script again!
    echo ============================================================
)

pause
