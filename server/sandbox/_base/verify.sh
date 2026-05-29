#!/bin/sh
# Reference verify script: copy read-only source to a writable workdir and
# assert it is non-empty. Real images replace the build/test section.
set -eu
WORK=/home/kungfu/work
mkdir -p "$WORK"
cp -a /src/. "$WORK"/ 2>/dev/null || cp -r /src/* "$WORK"/
cd "$WORK"
if [ -z "$(ls -A)" ]; then
  echo "no source provided" >&2
  exit 1
fi
echo "base sandbox: received $(ls -A | wc -l) entries; no language toolchain configured" >&2
exit 0
