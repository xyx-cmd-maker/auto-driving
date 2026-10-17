@echo off
rem ============================================================
rem  CARLA visual demo - one-click launcher
rem
rem  IMPORTANT 1: this file is ASCII-only ON PURPOSE. A .cmd saved
rem  as UTF-8 without BOM is decoded as GBK by cmd.exe on Chinese
rem  Windows and its comments turn into garbage commands.
rem
rem  IMPORTANT 2: do NOT use Test-NetConnection for the port probe.
rem  Measured on this machine it can hang for tens of seconds even
rem  when the port is already listening, which made the launcher
rem  look frozen at "[1/3] Checking CARLA server ...". We use a
rem  plain TcpClient connect with a short timeout instead (ms).
rem
rem  IMPORTANT 3: CARLA's spectator is a free camera and set_transform
rem  alone is not enough for API clients (the server's pygame event
rem  loop is idle), so the follow is driven by a background thread in
rem  the Python script. Watch the printed "camera moved" value.
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
rem Fast probe: single TcpClient connect, 800 ms budget.
powershell -NoProfile -Command "$c=New-Object System.Net.Sockets.TcpClient; try{ $a=$c.BeginConnect('127.0.0.1',2000,$null,$null); if($a.AsyncWaitHandle.WaitOne(800) -and $c.Connected){ exit 0 } else { exit 1 } } catch { exit 1 } finally { $c.Close() }"
if %errorlevel%==0 (
  echo       server already listening - reusing it
  goto server_ready
)

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
echo       foreground and the camera should follow it from behind (~9 m).
echo       The console prints how far the CAMERA itself travelled; that
echo       number should roughly equal the distance the car drove.
echo.
echo       NOTE: if a closed-loop experiment is running in the background,
echo       it also drives this same server. Stop it first for a clean demo.
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
