#!/bin/sh
# Oberon verify (OBNC). OBNC requires each module in a file named <Module>.obn.
# We flatten src/ and test/ into the workdir so imports resolve, then build and run
# the program module `Main` (the grader). Its ASSERTs trap on failure -> non-zero
# exit. OBNC compiles to C and links libgc; both are in the image, so this runs
# fully offline (--network none).
set -eu
WORK=/home/kungfu/work
rm -rf "$WORK"
mkdir -p "$WORK"
cp -a /src/. "$WORK"/ 2>/dev/null || cp -r /src/* "$WORK"/
cd "$WORK"

[ -d src ] && cp -f src/*.obn . 2>/dev/null || true
[ -d test ] && cp -f test/*.obn . 2>/dev/null || true
export OBNC_IMPORT_PATH="$WORK"

if [ -f Main.obn ]; then
  obnc Main.obn
  exec ./Main
fi

# No grader module: compile-check every module instead.
for m in *.obn; do obnc -c "$m"; done
