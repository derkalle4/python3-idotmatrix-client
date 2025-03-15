Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
$root = "$PSScriptRoot\.."
. "$root\venv\Scripts\Activate.ps1"
if (-not $?){
	Write-Host "ERROR: Failed to open venv, try running the setup script in the /windows_scripts/ of the git folder."
	exit
}
cd $root  # Python needs to open in the root of the git folder for relative paths to be correct.
python3 ".\gui.py"
pause
