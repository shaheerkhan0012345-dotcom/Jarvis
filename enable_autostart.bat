@echo off
setlocal
cd /d "%~dp0"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_VBS=%~dp0launch_jarvis_silent.vbs"

copy /Y "%TARGET_VBS%" "%STARTUP_FOLDER%\JarvisStartup.vbs" >nul

if %ERRORLEVEL% equ 0 (
    echo ============================================================
    echo [SUCCESS] JARVIS auto-start on PC boot has been ENABLED!
    echo JARVIS will now launch automatically in the background
    echo whenever your PC is turned on and you log in.
    echo ============================================================
) else (
    echo [ERROR] Could not register startup shortcut.
)
pause
