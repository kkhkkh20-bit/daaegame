#!/bin/bash
# Fast checks before any push: unit tests, override map, Ren'Py lint (on this folder).
#   RENPY_SDK=... dev/check.sh
cd "$(dirname "$0")/.." || exit 1
set -eo pipefail
python3 -m unittest discover -s dev -p "test_*.py" 2>&1 | tail -3
SDK=${RENPY_SDK:?set RENPY_SDK (dev/setup_sdk.sh)}
"$SDK/renpy.sh" . lint > /tmp/room13-lint.txt 2>&1 || true
# 0.18.56: parse errors print as File "game/x.rpy", line N: ... and were missed before.
if grep -E "\.rpy:[0-9]+ |\.rpy\", line [0-9]+:" /tmp/room13-lint.txt | grep -v "is not loadable"; then
  echo "lint: problems above (full log /tmp/room13-lint.txt)"; exit 1
fi
echo "lint: ok"
