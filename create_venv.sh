#!/bin/bash
set -e
# get the directory of file
IDO_DIR="$(dirname "$0")"
# create venv
python3 -m venv "$IDO_DIR/venv"
# enable venv
source "$IDO_DIR/venv/bin/activate"
# install dependencies from pyproject.toml
pip3 install "$IDO_DIR/"
