#!/bin/bash
set -e
# go to directory of file
IDO_DIR="$(dirname "$0")"

# activate venv
source "$IDO_DIR/venv/bin/activate"
# run app
python3 "$IDO_DIR/app.py" "$@"
