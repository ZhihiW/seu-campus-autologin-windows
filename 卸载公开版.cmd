@echo off
chcp 65001 >nul
set "SCRIPT_DIR=%~dp0"
set "UNINSTALLER=%SCRIPT_DIR%installer\uninstall.ps1"
if not exist "%UNINSTALLER%" set "UNINSTALLER=%LOCALAPPDATA%\SEUCampusAutoLoginOSS\uninstall.ps1"
if not exist "%UNINSTALLER%" (
  echo 未找到开源版卸载程序。
  pause
  exit /b 2
)
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%UNINSTALLER%"
if errorlevel 1 echo 卸载未完成，请查看上方错误信息。
pause
