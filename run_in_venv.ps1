$originalArgs = $args
$originalPath = Get-Location
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
	python "$root\app.py" $originalArgs
	Set-Location -Path $originalPath
}
