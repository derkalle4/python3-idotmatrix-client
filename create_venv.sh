#!/bin/bash

# go to directory of file
cd $(dirname "$0")
# create venv
python3 -m venv venv
# enable venv
source venv/bin/activate
# install dependencies from pyproject.toml
pip3 install .
