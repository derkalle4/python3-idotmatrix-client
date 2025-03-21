#!/bin/bash
set -e
# get directory of file
IDO_DIR="$(dirname "$0")"

# ensure we have the right global python
. "$IDO_DIR"/find_cmds.sh

# enable venv
# Check if the OS is Windows and choose the correct activation script
if [[ "$OSTYPE" == "msys" ]]; then
    # Windows Git Bash
    source "$IDO_DIR/venv/Scripts/activate"
    PYTHON_CMD_VENV="$IDO_DIR/venv/Scripts/$PYTHON_CMD"
else
    # POSIX (Linux, macOS, etc.)
    source "$IDO_DIR/venv/bin/activate"
    PYTHON_CMD_VENV="$IDO_DIR/venv/bin/$PYTHON_CMD"
fi
# todo: Check for binaries similar to find_cmds. A venv can be created with python3 but only contain pytgom on some systems

# run app
$PYTHON_CMD_VENV "$IDO_DIR/app.py" "$@"
