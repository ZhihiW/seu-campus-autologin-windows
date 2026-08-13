@echo off
chcp 65001 >nul
set "SCRIPT_DIR=%~dp0"
set "APP_EXE=%SCRIPT_DIR%app\SEUCampusAutoLoginOSS.exe"
if not exist "%APP_EXE%" set "APP_EXE=%LOCALAPPDATA%\SEUCampusAutoLoginOSS\app\SEUCampusAutoLoginOSS.exe"
if not exist "%APP_EXE%" (
  echo 未找到开源版程序，请先运行“安装公开版.cmd”。
  pause
  exit /b 2
)
"%APP_EXE%" run-once --initial-delay 0
pause
