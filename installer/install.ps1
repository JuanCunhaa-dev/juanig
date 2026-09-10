#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$repo = "https://github.com/JuanCunhaa-dev/juanig.git"
$destDir = Join-Path $env:LOCALAPPDATA "Programs\juanig"

function Find-Python {
  foreach ($candidate in @(
      { & py -3 -c "import sys; print(sys.executable)" 2>$null },
      { & python -c "import sys; print(sys.executable)" 2>$null },
      { & python3 -c "import sys; print(sys.executable)" 2>$null }
    )) {
    try {
      $path = & $candidate
      if ($LASTEXITCODE -eq 0 -and $path -and (Test-Path $path.Trim())) {
        return $path.Trim()
      }
    } catch { }
  }
  return $null
}

Write-Host "Installing juanig (Python launcher, no unsigned .exe)..."

$python = Find-Python
if (-not $python) {
  Write-Host "Python not found. Installing Python with winget..."
  winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
  $python = Find-Python
}
if (-not $python) {
  throw "Python is required. Install Python 3 from https://www.python.org/downloads/ and run this installer again."
}

Write-Host "Using $python"
& $python -m pip install --upgrade pip
& $python -m pip install --upgrade "git+$repo"
if ($LASTEXITCODE -ne 0) { throw "pip install failed." }

New-Item -ItemType Directory -Force -Path $destDir | Out-Null
$exePath = Join-Path $destDir "juanig.exe"
if (Test-Path $exePath) {
  Remove-Item $exePath -Force
  Write-Host "Removed blocked juanig.exe"
}

$cmdPath = Join-Path $destDir "juanig.cmd"
@"
@echo off
"$python" -m juanig %*
"@ | Set-Content -Path $cmdPath -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
if ($userPath -notlike "*$destDir*") {
  $trimmed = $userPath.TrimEnd(";")
  $next = if ($trimmed) { "$trimmed;$destDir" } else { $destDir }
  [Environment]::SetEnvironmentVariable("Path", $next, "User")
}
$env:Path = "$destDir;$env:Path"

& $python -m juanig --install-skills
Write-Host ""
Write-Host "juanig is ready: $cmdPath"
Write-Host "Open a new terminal, then run: juanig --help"
