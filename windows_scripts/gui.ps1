Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
$root = Resolve-Path -Path "$PSScriptRoot\.."
& "$root\run_in_venv.ps1" -DontInvokeApp "$root\gui.py"
pause
