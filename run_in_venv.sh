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


pwd_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)  # POSIX-safe script directory fetching. Details: https://stackoverflow.com/a/29835459
py_cmd=$(get_py)
# open venv
source "$venv_dir/activate"
# run app
$py_cmd "$pwd_dir/app.py" "$@"
