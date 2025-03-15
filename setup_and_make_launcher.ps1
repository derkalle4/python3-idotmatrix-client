# Starts by making sure the app is set up
echo "Setting up iDotMatrix..."

if (Test-Path -Path '.\gui.py') {
    echo "gui.py found, assuming the script has launched from the correct path."
} else {
    echo "`nERROR: gui.py not found!`nThis means that the script wasn't launched from the correct folder.`n"
    echo "To work correctly, you need to launch this script from the root folder of the iDotMatrix git folder."
    echo "To do this, open the folder this script is located in in Windws Explorer, right click the script, and press 'Run in powershell'.`n"
    echo "If that doesn't work, either open a powershell window and cd to the folder, or open the iDotMatrix git folder in Windows Explorer, then shift-right-click inside in an empty spot in the folder window, and click 'Open in powershell'."
    echo "With powershell open, write .\\setup_and_make_launcher.ps1 and press enter"
    pause
    exit
}

echo "This script will now open the VENV and install the required PIP dependencies."
if (Test-Path -Path '.\venv\Scripts\Activate.ps1') {
    echo "Venv set up, opening it."
} else {
    echo "Venv not set up, creating it. Make sure you have python installed."
    python3 -m venv venv
}

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\venv\Scripts\Activate.ps1
echo "Making sure PIP requirements are met, installs them if not."
python3 -m pip install ./
python3 -m pip install pyqt5
python3 -m pip install requests


echo "`nThis script will now create the shortcut on your desktop."

$WshShell = New-Object -COMObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\iDotMatrix GUI.lnk")
$Shortcut.TargetPath = '%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe'

$userInput = Read-Host -Prompt "`nDo you want the terminal to be hidden when launching the GUI?`n> [y/n]"
if ($userInput -eq "y") {
	$Shortcut.Arguments = '-WindowStyle Hidden -File ".\run.ps1"'  
	echo "If the GUI isn't opening, re-run this script without hiding the terminal, so you can see what went wrong."
} else {
	$Shortcut.Arguments = '-File ".\run.ps1"'  #-WindowStyle Hidden 
}

$Shortcut.WorkingDirectory = split-path -parent $MyInvocation.MyCommand.Definition
$Shortcut.Save()
echo "`n--------`nA shortcut should now have been created on your desktop. `nIf commands here fail, make sure you have Python installed, and see if you can open the GUI manually through powershell, by manually using the commands in this file."
pause
