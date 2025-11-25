$BackendRoot = "C:\Project\MarSci Project\MarSci Lite\backend"
$AppSrc = Join-Path $BackendRoot "phase2\app"
Write-Host "Running smoke tests against http://localhost:8000"

# 1) health
try {
    $h = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/healthz" -Method GET -TimeoutSec 5
    Write-Host "healthz:" $h.StatusCode $h.Content
} catch {
    Write-Host "healthz failed:" $_.Exception.Message
    exit 2
}

# 2) analyze sample
$payload = @{ kpi="CTR"; window=5; values = @(1,1,1,1,1); role="anon" } | ConvertTo-Json
try {
    $r = Invoke-RestMethod -Uri "http://localhost:8000/analyze" -Method POST -ContentType "application/json" -Body $payload -TimeoutSec 10
    Write-Host "analyze response keys:" ($r.PSObject.Properties | ForEach-Object Name) -ForegroundColor Green
    Write-Host ($r | ConvertTo-Json -Depth 3)
} catch {
    Write-Host "analyze failed:" $_.Exception.Message -ForegroundColor Red
    exit 3
}

Write-Host "SMOKE OK"
