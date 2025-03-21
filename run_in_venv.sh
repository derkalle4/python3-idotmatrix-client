#!/usr/bin/env bash
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

. "$IDO_DIR"/find_cmds.sh

# run app
$PYTHON_CMD "$IDO_DIR/app.py" "$@"
