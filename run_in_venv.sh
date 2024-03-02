#!/bin/bash
set -e
# get directory of file
IDO_DIR="$(dirname "$0")"
# activate venv
if [[ "$OSTYPE" == "msys" ]]; then
    # Windows Git Bash
    source "$IDO_DIR/venv/Scripts/activate"
else
    # POSIX (Linux, macOS, etc.)
    source "$IDO_DIR/venv/bin/activate"
fi

# run app
# Check if python3 is available, otherwise use python
if command -v python3 > /dev/null 2>&1; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# run app
$PYTHON_CMD "$IDO_DIR/app.py" "$@"
