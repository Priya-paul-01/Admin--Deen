@echo off
REM GreenCommute Dashboard HTTP Server - Windows launcher
REM Usage: double-click or run "start_server.bat" from command prompt

set SERVER_DIR=E:\Samsudeen\Hermes agent
set PORT=8080
set LOG_FILE=%SERVER_DIR%\server.log

cd /d "%SERVER_DIR%"

REM Kill any existing process on port 8080
powershell -Command "Get-NetTCPConnection -LocalPort %PORT% -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" 2>nul
timeout /t 1 /nobreak >nul

echo [%date% %time%] Starting GreenCommute Dashboard server on port %PORT%...
echo [%date% %time%] Server directory: %SERVER_DIR%

REM Start server in background, redirect output to log
start /B python -u -m http.server %PORT% --bind 127.0.0.1 >> "%LOG_FILE%" 2>&1

REM Give it a moment to start
timeout /t 2 /nobreak >nul

REM Verify it started
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:%PORT%/greencommute_dashboard.html' -UseBasicParsing; if (\$response.StatusCode -eq 200) { Write-Host '%date% %time% [OK] Server is RUNNING' -ForegroundColor Green; Write-Host '%date% %time% Access: http://127.0.0.1:%PORT%/greencommute_dashboard.html' -ForegroundColor Cyan } else { Write-Host '%date% %time% [FAIL] HTTP Status:' \$response.StatusCode -ForegroundColor Red } } catch { Write-Host '%date% %time% [FAIL] Server not responding' -ForegroundColor Red; exit /b 1 }"

echo.
echo Server log: %LOG_FILE%
echo.
pause
