#!/bin/bash
# Download Ren'Py 8.5.3 SDK once (about 200MB) and print its folder.
#   export RENPY_SDK=$(dev/setup_sdk.sh)
set -e
DIR=${RENPY_SDK_HOME:-$HOME/.cache/renpy}
SDK=$DIR/renpy-8.5.3-sdk
if [ ! -x "$SDK/renpy.sh" ]; then
  mkdir -p "$DIR"
  curl -sSL -o "$DIR/sdk.tar.bz2" https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.tar.bz2 >&2
  tar -xjf "$DIR/sdk.tar.bz2" -C "$DIR" >&2
  rm -f "$DIR/sdk.tar.bz2"
fi
echo "$SDK"
