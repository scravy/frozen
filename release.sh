#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
PYTHON_CMD=${PYTHON_CMD:-"python3"}

cd "${SCRIPT_DIR}" || exit
${PYTHON_CMD} -c 'import sys; assert sys.version_info[0:2] >= (3,11)' || exit

exec "${PYTHON_CMD}" -m twine upload --verbose dist/*
