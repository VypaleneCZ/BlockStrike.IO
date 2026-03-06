Param(
    [string]$InstallDir = "$env:LOCALAPPDATA\OmniMindAutomator"
)

$ErrorActionPreference = "Stop"

Write-Host "[1/5] Preparing installation folder: $InstallDir"
New-Item -Path $InstallDir -ItemType Directory -Force | Out-Null

Write-Host "[2/5] Copying project files"
$source = Resolve-Path (Join-Path $PSScriptRoot "..")
$excluded = @('.git', '.venv', '__pycache__', '.pytest_cache')
Get-ChildItem -Path $source -Force | Where-Object { $excluded -notcontains $_.Name } | ForEach-Object {
    $target = Join-Path $InstallDir $_.Name
    if ($_.PSIsContainer) {
        Copy-Item $_.FullName -Destination $target -Recurse -Force
    } else {
        Copy-Item $_.FullName -Destination $target -Force
    }
}

Write-Host "[3/5] Creating virtual environment"
python -m venv "$InstallDir\.venv"

Write-Host "[4/5] Installing dependencies"
& "$InstallDir\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$InstallDir\.venv\Scripts\python.exe" -m pip install -r "$InstallDir\requirements.txt"

Write-Host "[5/5] Creating desktop shortcut"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "OmniMind Automator.lnk"
$targetPath = Join-Path $InstallDir "launch_omnimind.bat"

$wShell = New-Object -ComObject WScript.Shell
$shortcut = $wShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.WorkingDirectory = $InstallDir
$shortcut.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,220"
$shortcut.Description = "Launch OmniMind Automator"
$shortcut.Save()

Write-Host "Installation complete. Shortcut created: $shortcutPath"
Write-Host "Use the desktop icon 'OmniMind Automator' for quick launch."
