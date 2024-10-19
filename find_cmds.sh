#!/bin/bash
export PYTHON_CMD

if [ -z "$PYTHON_CMD" ]; then

	if command -v python3 &>/dev/null; then
		PYTHON_CMD=python3
	else
		if command -v python &>/dev/null; then
			PYTHON_CMD=python
		else
			echo "Python not found" >&2
			exit 1
		fi
	fi
fi
