#!/usr/bin/env bash
set -e

get_py() {
    if command -v python3 &>/dev/null; then
        echo "python3"
        return 0
    fi
    if command -v python &>/dev/null; then
        echo "python"
        return 0
    fi
    echo "Python not found" >&2
    return 1
}

get_venv_dir() {
    local pwd_dir="$1"
    if [[ "$OSTYPE" == "msys" ]]; then
        # Windows Bash (msys, git bash)
        echo "$pwd_dir/venv/Scripts"
        return 0
    else
        # POSIX (Linux, macOS, etc.)
        echo "$pwd_dir/venv/bin"
        return 0
    fi
}

get_venv_py() {
    # find and return a direct path to the python binary in the venv.
    # this ensures we're not calling the global python binary,
    # which can sometimes happen depending on the system.
    local venv_dir="$1"
    test -f "$venv_dir/python3" && echo "$venv_dir/python3" && return 0
    test -f "$venv_dir/python"  && echo "$venv_dir/python"  && return 0
    test -f "$venv_dir/py3"     && echo "$venv_dir/py3"     && return 0
    test -f "$venv_dir/py"      && echo "$venv_dir/py"      && return 0
    echo "Python not found in venv, was it correctly set up?" >&2
    return 1
}


pwd_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)  # POSIX-safe script directory fetching. Details: https://stackoverflow.com/a/29835459
py_cmd=$(get_py)
# open venv
source "$venv_dir/activate"
# make sure we use the python binary belonging to the venv
venv_py_cmd=$(get_venv_py "$venv_dir")
# run app
$venv_py_cmd "$pwd_dir/app.py" "$@"
