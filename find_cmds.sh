#!/bin/bash
export PYTHON_CMD
export PIP_CMD

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

if [ -z "$PIP_CMD" ]; then

	if command -v pip3 &>/dev/null; then
		PIP_CMD=pip3
	else
		if command -v pip &>/dev/null; then
			PIP_CMD=python
		else
			echo "Pip not found" >&2
			exit 1
		fi
	fi
fi
