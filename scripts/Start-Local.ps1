$ErrorActionPreference = 'Stop'
$btgRoot = Split-Path -Parent $PSScriptRoot
$btgPrivate = Join-Path $btgRoot 'app\private'
$btgUrl = 'http://127.0.0.1:8000'
New-Item -ItemType Directory -Path $btgPrivate -Force | Out-Null

function Test-BtgHealth {
    try {
        $btgResponse = Invoke-RestMethod -Uri "$btgUrl/api/health" -TimeoutSec 2
        return ($btgResponse.status -eq 'ok')
    } catch { return $false }
}

if (-not (Test-BtgHealth)) {
    $btgPython = (Get-Command python -ErrorAction Stop).Source
    $btgProcess = Start-Process -FilePath $btgPython -ArgumentList @('app/server.py', '--demo') `
        -WorkingDirectory $btgRoot -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $btgPrivate 'server.stdout.log') `
        -RedirectStandardError (Join-Path $btgPrivate 'server.stderr.log')
    $btgProcess.Id | Set-Content -LiteralPath (Join-Path $btgPrivate 'server.pid')
    $btgDeadline = (Get-Date).AddSeconds(15)
    while ((Get-Date) -lt $btgDeadline) {
        if (Test-BtgHealth) { break }
        Start-Sleep -Milliseconds 300
    }
    if (-not (Test-BtgHealth)) {
        throw "The local server did not start. See app/private/server.stderr.log."
    }
}
Start-Process $btgUrl
Write-Output 'Beyond the Game is running. Credentials: app/private/demo-access.txt'
