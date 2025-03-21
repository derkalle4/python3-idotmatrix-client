param(
    [switch]$DontInvokeApp  # Used to pass args directly to python, not app.py, e.g. for installing non-standard pip packages.
    )

$originalArgs = $args
$originalPath = Get-Location
& {
    $root = $PSScriptRoot
    Set-Location -Path "$root"

    $likelyCorrectPath = Test-Path -Path "$root\app.py" -PathType Leaf
    if (-not $likelyCorrectPath){
        Write-Host "ERROR: The script seems to have been run from the wrong path. Try right-clicking the .ps1 file and clicking 'run with powershell'."
        Set-Location -Path $originalPath
        pause
        exit
    }


    $venvAlreadyExists = Test-Path -Path "$root\venv_windows\Scripts\Activate.ps1" -PathType Leaf
    if (-not $venvAlreadyExists) {
        Write-Host "Venv for Windows doesn't exist, creating it. "
        python -m venv "$root\venv_windows"
        if (-not $?){
            Write-Host "`nERROR: Failed to create venv, exiting program. Make sure Python is installed."
            Set-Location -Path $originalPath
            pause
            exit
        }
        Write-Host "Venv created."
    }


    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
    . "$root\venv_windows\Scripts\Activate.ps1"
    if (-not "$?"){
        Write-Host "ERROR: Failed to open venv. Make sure Python is installed, then try this script again."
        Set-Location -Path $originalPath
        pause
        exit
    }

    $py_cmd = "python"
    if (Test-Path -Path "$root/venv_windows/Scripts/python3.exe" -PathType Leaf ){
        $py_cmd = "$root/venv_windows/Scripts/python3.exe"
    } elseif (Test-Path -Path "$root/venv_windows/Scripts/python.exe" -PathType Leaf){
        $py_cmd = "$root/venv_windows/Scripts/python.exe"
    } else {
        Write-Host "ERROR: Failed to find venv's python executable, try re-making the venv by deleting the 'venv_windows' folder and running build.ps1."
        Set-Location -Path $originalPath
        pause
        exit
    }

    if (-not $venvAlreadyExists){
        Write-Host "Installing dependencies into venv."
        & $py_cmd -m pip install "$root/"
    }

    if ($DontInvokeApp){
        & $py_cmd $originalArgs
    } else {
        & $py_cmd "$root/app.py" $originalArgs
    }

    Set-Location -Path $originalPath

}
