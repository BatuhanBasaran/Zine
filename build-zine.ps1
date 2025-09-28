# build-zine.ps1
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcDir   = Join-Path $repoRoot 'plugin.video.zine'
$outZip   = Join-Path $repoRoot 'plugin.video.zine.zip'

if (-not (Test-Path $srcDir)) { throw "Quellordner nicht gefunden: $srcDir" }
if (Test-Path $outZip) { Remove-Item $outZip -Force }

Add-Type -AssemblyName System.IO.Compression.FileSystem

# entspricht Explorer: Ordner plugin.video.zine ist Root im ZIP,
# inkl. Leerordnern und Standardattributen
[IO.Compression.ZipFile]::CreateFromDirectory(
    $srcDir,
    $outZip,
    [IO.Compression.CompressionLevel]::Optimal,
    $true  # includeBaseDirectory
)

Write-Host "Fertig: $outZip"
