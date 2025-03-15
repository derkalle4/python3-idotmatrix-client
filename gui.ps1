Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\venv\Scripts\Activate.ps1
python3 gui.py
pause  # This prevents the terminal from closing when Python closes. Its useful for reading errors without opening a new terminal, but it will leave the terminal open when the script is opened with a hidden window.
