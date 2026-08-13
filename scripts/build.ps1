param(
    [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VersionFile = Join-Path $ProjectRoot "src\seu_autologin\__init__.py"
$VersionText = Get-Content -LiteralPath $VersionFile -Raw -Encoding UTF8
if ($VersionText -notmatch '__version__\s*=\s*"([^"]+)"') {
    throw "无法从 $VersionFile 读取版本号。"
}
$Version = $Matches[1]
$BuildDir = Join-Path $ProjectRoot "build"
$DistDir = Join-Path $ProjectRoot "dist"
$ReleaseDir = Join-Path $ProjectRoot "release"
$PackageName = "SEUCampusAutoLoginOSS-$Version-windows-x64"
$PackageDir = Join-Path $ReleaseDir $PackageName

foreach ($Target in @($BuildDir, $DistDir, $ReleaseDir)) {
    $FullTarget = [IO.Path]::GetFullPath($Target)
    $FullRoot = [IO.Path]::GetFullPath($ProjectRoot).TrimEnd('\') + '\'
    if (-not $FullTarget.StartsWith($FullRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "拒绝清理项目目录之外的路径：$FullTarget"
    }
    if (Test-Path -LiteralPath $FullTarget) {
        Remove-Item -LiteralPath $FullTarget -Recurse -Force
    }
}

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --console `
    --name SEUCampusAutoLoginOSS `
    --paths (Join-Path $ProjectRoot "src") `
    --collect-all playwright `
    --hidden-import win32timezone `
    --distpath $DistDir `
    --workpath $BuildDir `
    --specpath $BuildDir `
    (Join-Path $ProjectRoot "packaging\entrypoint.py")
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller 构建失败。"
}

New-Item -ItemType Directory -Path (Join-Path $PackageDir "app") -Force | Out-Null
Copy-Item -Path (Join-Path $DistDir "SEUCampusAutoLoginOSS\*") -Destination (Join-Path $PackageDir "app") -Recurse -Force
Copy-Item -LiteralPath (Join-Path $ProjectRoot "installer") -Destination (Join-Path $PackageDir "installer") -Recurse -Force
foreach ($Name in @(
    "安装公开版.cmd",
    "配置公开版.cmd",
    "手动检查.cmd",
    "立即运行一次.cmd",
    "卸载公开版.cmd",
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "PRIVACY.md",
    "THIRD_PARTY_NOTICES.md"
)) {
    Copy-Item -LiteralPath (Join-Path $ProjectRoot $Name) -Destination (Join-Path $PackageDir $Name) -Force
}

$ZipPath = Join-Path $ReleaseDir "$PackageName.zip"
Compress-Archive -LiteralPath $PackageDir -DestinationPath $ZipPath -CompressionLevel Optimal
$Hash = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
Set-Content -LiteralPath "$ZipPath.sha256" -Value "$Hash  $PackageName.zip" -Encoding ascii

Write-Host "构建完成：$ZipPath" -ForegroundColor Green
Write-Host "SHA256：$Hash"
