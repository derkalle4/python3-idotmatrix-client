#!/bin/bash
set -e
# get the directory of the file
IDO_DIR="$(dirname "$0")"

. "$IDO_DIR"/find_cmds.sh

# create venv
$PYTHON_CMD -m venv "$IDO_DIR/venv"

# enable venv
# Check if the OS is Windows and choose the correct activation script
if [[ "$OSTYPE" == "msys" ]]; then
    # Windows Git Bash
    source "$IDO_DIR/venv/Scripts/activate"
else
    # POSIX (Linux, macOS, etc.)
    source "$IDO_DIR/venv/bin/activate"
fi

# install dependencies from pyproject.toml
$PYTHON_CMD -m $PIP_CMD install "$IDO_DIR/"
