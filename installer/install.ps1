#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$repo = "Juancunhaa-dev/juanig"
$destDir = Join-Path $env:LOCALAPPDATA "Programs\juanig"
$exePath = Join-Path $destDir "juanig.exe"
$releaseApi = "https://api.github.com/repos/$repo/releases/latest"

Write-Host "Installing juanig..."
New-Item -ItemType Directory -Force -Path $destDir | Out-Null

$release = Invoke-RestMethod -Uri $releaseApi -Headers @{ "User-Agent" = "juanig-installer" }
$asset = $release.assets | Where-Object { $_.name -eq "juanig.exe" } | Select-Object -First 1
if (-not $asset) { throw "juanig.exe was not found in the latest GitHub release." }

Write-Host "Downloading $($release.tag_name)..."
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $exePath

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
if ($userPath -notlike "*$destDir*") {
  $trimmed = $userPath.TrimEnd(";")
  $next = if ($trimmed) { "$trimmed;$destDir" } else { $destDir }
  [Environment]::SetEnvironmentVariable("Path", $next, "User")
}
$env:Path = "$destDir;$env:Path"

& $exePath --install-skills
Write-Host ""
Write-Host "juanig is ready: $exePath"
Write-Host "Open a new terminal, then run: juanig --help"
