$og_args = $args
& {
	Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
	$root = $PSScriptRoot
	. "$root\venv\Scripts\Activate.ps1"
	if (-not "$?"){
		Write-Host "ERROR: Failed to open venv, try running the setup script in the /windows_scripts/ of the git folder."
		exit
		pause
	}
	Set-Location -Path $root
	python3 "$root\app.py" $og_args
	#Set-Location -Path $originalDir
}
