param(
    [switch]$SkipCurrentTest
)

$ErrorActionPreference = "Stop"

$TaskName = "SEU Campus Auto Login OSS"
$AppName = "SEUCampusAutoLoginOSS"
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackageRoot = Split-Path -Parent $SourceDir
$SourceAppDir = Join-Path $PackageRoot "app"
$SourceExe = Join-Path $SourceAppDir "SEUCampusAutoLoginOSS.exe"
$InstallDir = Join-Path $env:LOCALAPPDATA $AppName
$InstallAppDir = Join-Path $InstallDir "app"
$InstalledExe = Join-Path $InstallAppDir "SEUCampusAutoLoginOSS.exe"
$PowerShellExe = Join-Path $PSHOME "powershell.exe"
$StartupLink = Join-Path ([Environment]::GetFolderPath("Startup")) "SEU Campus Auto Login OSS.lnk"
$StartMenuDir = Join-Path ([Environment]::GetFolderPath("Programs")) "SEU Campus Auto Login OSS"

Write-Host "=== 东南大学校园网自动登录开源版安装向导 ===" -ForegroundColor Cyan
Write-Host "本程序是非官方学生项目，仅支持固定门户 http://10.9.10.100/。" -ForegroundColor Yellow
Write-Host "该门户使用 HTTP，凭据传输不具备 TLS 保护。" -ForegroundColor Yellow

if (-not (Test-Path -LiteralPath $SourceExe)) {
    throw "安装包不完整，未找到：$SourceExe"
}

New-Item -ItemType Directory -Path $InstallAppDir -Force | Out-Null
Copy-Item -Path (Join-Path $SourceAppDir "*") -Destination $InstallAppDir -Recurse -Force

New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $SourceDir "uninstall.ps1") -Destination (Join-Path $InstallDir "uninstall.ps1") -Force

& $InstalledExe configure
if ($LASTEXITCODE -ne 0) {
    throw "凭据配置未完成，尚未注册自动登录任务。"
}

$Action = New-ScheduledTaskAction -Execute $InstalledExe -Argument "run-once" -WorkingDirectory $InstallAppDir
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$Principal = New-ScheduledTaskPrincipal `
    -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive `
    -RunLevel Limited

$TaskInstalled = $false
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -Description "登录 Windows 后检测并自动认证东南大学校园网（非官方开源版）" `
        -Force | Out-Null
    $TaskInstalled = $true
}
catch {
    Write-Warning "任务计划注册失败，将使用当前用户启动文件夹：$($_.Exception.Message)"
    $Shell = New-Object -ComObject WScript.Shell
    $Shortcut = $Shell.CreateShortcut($StartupLink)
    $Shortcut.TargetPath = $InstalledExe
    $Shortcut.Arguments = "run-once"
    $Shortcut.WorkingDirectory = $InstallAppDir
    $Shortcut.Description = "东南大学校园网自动登录开源版"
    $Shortcut.Save()
}

New-Item -ItemType Directory -Path $StartMenuDir -Force | Out-Null
$Shell = New-Object -ComObject WScript.Shell
$Commands = @(
    @{ Name = "配置凭据.lnk"; Target = $InstalledExe; Arguments = "configure" },
    @{ Name = "检查状态.lnk"; Target = $InstalledExe; Arguments = "check" },
    @{ Name = "立即运行一次.lnk"; Target = $InstalledExe; Arguments = "run-once --initial-delay 0" },
    @{
        Name = "卸载.lnk"
        Target = $PowerShellExe
        Arguments = "-NoLogo -NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $InstallDir 'uninstall.ps1')`""
    }
)
foreach ($Command in $Commands) {
    $Shortcut = $Shell.CreateShortcut((Join-Path $StartMenuDir $Command.Name))
    $Shortcut.TargetPath = $Command.Target
    $Shortcut.Arguments = $Command.Arguments
    $Shortcut.WorkingDirectory = $InstallDir
    $Shortcut.Save()
}

if (-not $SkipCurrentTest) {
    Write-Host "正在进行不会断网、不会重启的当前状态测试……" -ForegroundColor Cyan
    & $InstalledExe run-once --initial-delay 0 --network-wait-seconds 0 --no-browser-fallback
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "当前状态测试未通过；安装仍已完成，请从开始菜单运行“检查状态”。"
    }
}

if ($TaskInstalled) {
    Write-Host "安装完成：已注册任务计划“$TaskName”。" -ForegroundColor Green
}
else {
    Write-Host "安装完成：已创建当前用户启动快捷方式。" -ForegroundColor Green
}
Write-Host "公开版安装目录：$InstallDir"
Write-Host "私人版本的文件、凭据和任务计划均未修改。"
