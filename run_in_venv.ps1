# PowerShell idot script
$ErrorActionPreference = "Stop" # Similar to 'set -e' in bash

# Get the directory of the script
$IDO_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Activate venv
& "$IDO_DIR\venv\Scripts\Activate.ps1"

# Run app.py with all passed arguments
python "$IDO_DIR\app.py" @args
