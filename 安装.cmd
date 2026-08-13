@echo off
chcp 65001 >nul
set "SCRIPT_DIR=%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%installer\install.ps1"
if errorlevel 1 echo 安装未完成，请查看上方错误信息。
pause
