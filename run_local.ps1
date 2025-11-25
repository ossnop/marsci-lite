Write-Host "=== MarSci Lite Local Backend Runner (fixed redirect) ==="

$BackendRoot = "C:\Project\MarSci Project\MarSci Lite\backend"
$AppPath     = Join-Path $BackendRoot "phase2\app"
$VenvPath    = Join-Path $BackendRoot ".venv"
$PythonExe   = Join-Path $VenvPath "Scripts\python.exe"
$LogStd      = Join-Path $BackendRoot "uvicorn.stdout.log"
$LogErr      = Join-Path $BackendRoot "uvicorn.stderr.log"

if (!(Test-Path $PythonExe)) { Write-Host "ERROR: venv python not found" -ForegroundColor Red; exit 1 }

# stop previous
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# start uvicorn, send stdout -> uvicorn.stdout.log and stderr -> uvicorn.stderr.log
$args = "-m uvicorn app.main:app --host 0.0.0.0 --port 8000"
Start-Process -FilePath $PythonExe -ArgumentList $args -WorkingDirectory $AppPath -NoNewWindow -RedirectStandardOutput $LogStd -RedirectStandardError $LogErr

Start-Sleep -Seconds 2
Write-Host "Started uvicorn; stdout:$LogStd stderr:$LogErr"
