@echo off
chcp 65001 >nul
set "SCRIPT_DIR=%~dp0"
set "APP_EXE=%SCRIPT_DIR%app\SEUCampusAutoLoginOSS.exe"
if not exist "%APP_EXE%" set "APP_EXE=%LOCALAPPDATA%\SEUCampusAutoLoginOSS\app\SEUCampusAutoLoginOSS.exe"
if not exist "%APP_EXE%" (
  echo 未找到程序，请先运行“安装.cmd”。
  pause
  exit /b 2
)

"%APP_EXE%" check
echo.
choice /C YN /N /M "是否立即执行一次认证？[Y/N] "
if errorlevel 2 goto END
"%APP_EXE%" run-once --initial-delay 0

:END
pause
