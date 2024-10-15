#!/usr/bin/env bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
PYTHON_CMD=${PYTHON_CMD:-"python3"}

cd "${SCRIPT_DIR}" || exit
${PYTHON_CMD} -c 'import sys; assert sys.version_info[0:2] >= (3,11), "python version mismatch"' || exit

${PYTHON_CMD} -m black src
${PYTHON_CMD} -m black test

echo ""
${PYTHON_CMD} -m flake8 --ignore=E704,E731,W503 --max-line-length=120 src \
  && echo "✅ flake8 good" || echo "❌ flake8 failed"

echo ""
${PYTHON_CMD} -m pylint --disable=C,R,fixme src \
  && PYTHONPATH=src ${PYTHON_CMD} -m pylint --disable=C,R test/*.py \
  && echo "✅ pylint good" || echo "❌ pylint failed"

${PYTHON_CMD} -m mypy --enable-incomplete-feature=NewGenericSyntax src/ \
  && PYTHONPATH=src ${PYTHON_CMD} -m mypy --enable-incomplete-feature=NewGenericSyntax test/ \
  && echo "✅ mypy good" || echo "❌ mypy failed"

${PYTHON_CMD} -m pytest \
  && echo "✅ pytest good" || echo "❌ pytest failed"
