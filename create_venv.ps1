# Equivalent PowerShell script
$ErrorActionPreference = "Stop" # Similar to 'set -e'

$IDO_DIR = $PSScriptRoot # Getting the script's directory

# Create venv
python -m venv "$IDO_DIR\venv"

# Enable venv
& "$IDO_DIR\venv\Scripts\Activate.ps1"

# Install dependencies from pyproject.toml
pip install "$IDO_DIR\"
