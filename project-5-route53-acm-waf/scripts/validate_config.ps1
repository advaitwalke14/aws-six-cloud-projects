$ErrorActionPreference = "Stop"
Write-Host "Running Project 5 local simulation and tests. No AWS resources will be created."
py .\simulate_failover.py
if ($LASTEXITCODE -ne 0) { throw "Simulation failed." }
py -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Unit tests failed." }
py .\scripts\validate_config.py
if ($LASTEXITCODE -ne 0) { throw "Config validation failed." }
Write-Host "Project 5 local checks completed successfully."
