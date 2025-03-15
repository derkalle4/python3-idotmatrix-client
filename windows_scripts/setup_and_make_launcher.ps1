# Starts by making sure the app is set up
Write-Host "Setting up iDotMatrix..."
Write-Host "(If something goes wrong, try running the script with an administrator instance of Powershell)"

$root = "$PSScriptRoot\.."
Write-Host "Launching from: $root"

if (Test-Path -Path "$root\gui.py") {
	Write-Host "gui.py found, assuming the script has launched from the correct path."
} else {
	Write-Host "`nERROR: gui.py not found!`nThis means that the script wasn't launched from the correct folder.`n"
		Write-Host "To work correctly, you need to launch this script from the root folder of the iDotMatrix git folder."
		Write-Host "To do this, open the folder this script is located in in Windws Explorer, right click the script, and press 'Run in powershell'.`n"
		Write-Host "If that doesn't work, either open a powershell window and cd to the folder, or open the iDotMatrix git folder in Windows Explorer, then shift-right-click inside in an empty spot in the folder window, and click 'Open in powershell'."
    Write-Host "With powershell open, write .\windows_scripts\setup_and_make_launcher.ps1 and press enter"
    pause
    exit
}

Write-Host "This script will now open the VENV and install the required PIP dependencies."
if (Test-Path -Path "$root\venv\Scripts\Activate.ps1") {
    Write-Host "Venv set up, opening it."
} else {
    Write-Host "Venv not set up, creating it. Make sure you have python installed."
    python3 -m venv venv
}

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
. "$root\venv\Scripts\Activate.ps1"
if (-not $?){
	Write-Host "ERROR: Failed to open venv, exiting program. Make sure Python is installed."
	exit
}
Write-Host "Making sure PIP requirements are met, installs them if not."
python3 -m pip install ./
python3 -m pip install pyqt5
python3 -m pip install requests


Write-Host "`nThis script will now create the shortcut on your desktop."

$WshShell = New-Object -COMObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\iDotMatrix GUI.lnk")
$Shortcut.TargetPath = "%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe"

$userInput = Read-Host -Prompt "`nDo you want the terminal to be hidden when launching the GUI?`n> [y/n]"
if ($userInput -eq "y") {
	$Shortcut.Arguments = "-WindowStyle Hidden -File `"$root\windows_scripts\gui.ps1`""
	Write-Host "If the GUI isn't opening, re-run this script without hiding the terminal, so you can see what went wrong."
} else {
	$Shortcut.Arguments = "-File `"$root\windows_scripts\gui.ps1`""  #-WindowStyle Hidden 
}

$Shortcut.IconLocation = "$root\idmc.ico"
$Shortcut.WorkingDirectory = split-path -parent $MyInvocation.MyCommand.Definition
$Shortcut.Save()
Write-Host "`n--------`nA shortcut should now have been created on your desktop. `nIf some commands in the script fails, first re-run without a hidden terminal if you chose to hide it, then make sure you have Python installed, and see if you can open the GUI manually through powershell, by manually using the commands in this file."
Write-Host "(If something went wrong, try running the script with an administrator instance of Powershell)"
pause
