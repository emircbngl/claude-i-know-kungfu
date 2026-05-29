#!/bin/sh
# Python verify: byte-compile everything, then run pytest if tests are present.
set -eu
WORK=/home/kungfu/work
mkdir -p "$WORK"
cp -a /src/. "$WORK"/ 2>/dev/null || cp -r /src/* "$WORK"/
cd "$WORK"

python -m compileall -q .

# Run pytest if any test files exist anywhere in the tree (not just the root).
# pytest exit code 5 means "no tests collected" — that is not a failure here,
# since compileall already proved the code compiles.
if [ -d tests ] || find . -name 'test_*.py' -type f | grep -q .; then
  rc=0
  python -m pytest -q || rc=$?
  [ "$rc" -eq 5 ] && exit 0
  exit "$rc"
fi
