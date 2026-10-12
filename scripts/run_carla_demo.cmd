@echo off
rem ============================================================
rem  CARLA 目视确认演示 —— 一键启动（双击即可）
rem
rem  为什么需要它：CARLA 的 spectator 是自由相机、不跟随车辆，
rem  实测 ego 走 82.5 m 而相机不动、二者相距 763 m —— 所以默认
rem  窗口里看到的是地图别处的静止场景，容易误判成"车没动"。
rem  本脚本会：① 启动服务端（若未运行）② 等端口就绪 ③ 开着相机跟随跑演示
rem
rem  用法：双击运行；或在命令行 `run_carla_demo.cmd 60` 指定秒数
rem ============================================================
setlocal
set CARLA_EXE=D:\CARLA\CarlaUE4.exe
set SCRIPT=%~dp0demo_carla_drive.py
set SECONDS=%1
if "%SECONDS%"=="" set SECONDS=60

if not exist "%CARLA_EXE%" (
  echo [错误] 找不到 CARLA 服务端：%CARLA_EXE%
  echo         请确认 CARLA 0.9.16 已装在 D:\CARLA
  pause
  exit /b 1
)
if not exist "%SCRIPT%" (
  echo [错误] 找不到演示脚本：%SCRIPT%
  pause
  exit /b 1
)

echo [1/3] 检查 CARLA 服务端是否在运行（端口 2000）...
powershell -NoProfile -Command "if((Test-NetConnection -ComputerName 127.0.0.1 -Port 2000 -WarningAction SilentlyContinue).TcpTestSucceeded){exit 0}else{exit 1}"
if %errorlevel%==0 (
  echo       已在运行
) else (
  echo       未运行，正在启动（首次就绪约 10-25 秒）...
  start "" "%CARLA_EXE%" -quality-level=Low -windowed -carla-port=2000
  powershell -NoProfile -Command "$ok=$false; for($i=0;$i -lt 60 -and -not $ok;$i++){ Start-Sleep -Seconds 2; $c=New-Object System.Net.Sockets.TcpClient; try{ $a=$c.BeginConnect('127.0.0.1',2000,$null,$null); if($a.AsyncWaitHandle.WaitOne(800) -and $c.Connected){$ok=$true} } catch {} finally { $c.Close() } }; if($ok){ Write-Host '       服务端就绪'; exit 0 } else { Write-Host '       等待超时'; exit 1 }"
  if not %errorlevel%==0 (
    echo [错误] 服务端未在 120 秒内就绪
    pause
    exit /b 1
  )
)

echo.
echo [2/3] 跑演示（%SECONDS% 秒）——请看 CarlaUE4 窗口，应能看到自车在动
echo       ^(相机跟在车后约 9 m；若窗口里是静止场景，说明跟随没生效^)
echo.
py -3.12 "%SCRIPT%" --seconds %SECONDS%
set RC=%errorlevel%

echo.
echo [3/3] 演示结束（退出码 %RC%）
echo       注意：CARLA 服务端仍在后台运行。要关掉它：
echo       Stop-Process -Name CarlaUE4,CarlaUE4-Win64-Shipping -Force
echo.
pause
endlocal
