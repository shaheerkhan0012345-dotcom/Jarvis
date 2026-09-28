@echo off
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

if exist "%STARTUP_FOLDER%\JarvisStartup.vbs" (
    del "%STARTUP_FOLDER%\JarvisStartup.vbs"
    echo ============================================================
    echo [SUCCESS] JARVIS auto-start has been DISABLED.
    echo ============================================================
) else (
    echo [INFO] JARVIS auto-start was not enabled.
)
pause
