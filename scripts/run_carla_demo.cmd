@echo off
rem ============================================================
rem  CARLA visual demo - one-click launcher
rem
rem  IMPORTANT: this file is ASCII-only ON PURPOSE.
rem  A .cmd file saved as UTF-8 without BOM is decoded as GBK by
rem  cmd.exe on Chinese Windows; Chinese comments then turn into
rem  garbage commands ("... is not recognized as an internal or
rem  external command"). Keep launchers ASCII.
rem
rem  CARLA's spectator is a free camera. set_transform alone is not
rem  enough for API clients (pygame's event loop is idle), so the
rem  follow is driven by a background thread inside the Python
rem  script. Watch the printed "camera moved" value to confirm.
rem
rem  Usage: double-click, or: run_carla_demo.cmd 60
rem ============================================================
setlocal
set CARLA_EXE=D:\CARLA\CarlaUE4.exe
set SCRIPT=%~dp0demo_carla_drive.py
set SECONDS=%1
if "%SECONDS%"=="" set SECONDS=60

if not exist "%CARLA_EXE%" (
  echo [ERROR] CARLA server not found: %CARLA_EXE%
  pause
  exit /b 1
)
if not exist "%SCRIPT%" (
  echo [ERROR] demo script not found: %SCRIPT%
  pause
  exit /b 1
)

echo [1/3] Checking CARLA server on port 2000 ...
powershell -NoProfile -Command "if((Test-NetConnection -ComputerName 127.0.0.1 -Port 2000 -WarningAction SilentlyContinue).TcpTestSucceeded){exit 0}else{exit 1}"
if %errorlevel%==0 goto server_ready

echo       not running, starting server ^(ready in ~10-25 s^) ...
start "" "%CARLA_EXE%" -quality-level=Low -windowed -carla-port=2000
powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 60 -and -not $ok;$i++){ Start-Sleep -Seconds 2; $c=New-Object System.Net.Sockets.TcpClient; try{ $a=$c.BeginConnect('127.0.0.1',2000,$null,$null); if($a.AsyncWaitHandle.WaitOne(800) -and $c.Connected){$ok=$true} } catch {} finally { $c.Close() } }; if($ok){ exit 0 } else { exit 1 }"
if not %errorlevel%==0 (
  echo [ERROR] server not ready within 120 s
  pause
  exit /b 1
)

:server_ready
echo       server is up
echo.
echo [2/3] Running demo for %SECONDS% s ...
echo       LOOK AT THE CarlaUE4 WINDOW: the ego car should be visible in the
echo       foreground, and the camera should follow it from behind (~9 m).
echo       The console also prints how far the CAMERA itself travelled;
echo       that number should roughly equal the distance the car drove.
echo.
py -3.12 "%SCRIPT%" --seconds %SECONDS%
set RC=%errorlevel%

echo.
echo [3/3] Demo finished ^(exit code %RC%^)
echo       The CARLA server keeps running in the background. To stop it:
echo       Stop-Process -Name CarlaUE4,CarlaUE4-Win64-Shipping -Force
echo.
pause
endlocal
