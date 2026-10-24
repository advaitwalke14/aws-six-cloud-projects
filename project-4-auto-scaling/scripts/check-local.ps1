$ErrorActionPreference = 'Stop'
Write-Host 'Running local Project 4 simulation...'
py .\chaos_simulation.py
if ($LASTEXITCODE -ne 0) { throw 'Simulation failed.' }
Write-Host 'Simulation process completed. This does not validate live AWS resources.'
