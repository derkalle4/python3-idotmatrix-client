#!/bin/bash
set -e
# go to directory of file
cd $(dirname "$0")
# activate venv
source venv/bin/activate
# run app
python3 app.py $@
