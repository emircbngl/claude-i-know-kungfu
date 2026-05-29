#!/bin/sh
# Gleam verify: run the task using the prebuilt template's resolved dependencies
# so the common case (stdlib + gleeunit) builds offline (--network none).
#
# The template at /opt/app was created and compiled at image-build time, so it
# carries a locked manifest.toml and build/packages. We use it as the BASE and
# overlay the task on top: a task that brings its OWN gleam.toml / manifest.toml
# is respected (not clobbered); a bare snippet inherits the template's locked
# stdlib+gleeunit. Dependencies beyond the cached set cannot be fetched offline;
# that case is reported clearly rather than as a code error.
set -eu
WORK=/home/kungfu/work
rm -rf "$WORK"
mkdir -p "$WORK"

# 1) Base = warmed template (gleam.toml + manifest.toml + build/packages).
cp -a /opt/app/. "$WORK"/
# 2) Drop the template's sample modules + their compiled output (keep build/packages).
rm -rf "$WORK"/src "$WORK"/test "$WORK"/build/dev
# 3) Overlay the task's files; a task-provided gleam.toml/manifest.toml wins.
cp -a /src/. "$WORK"/

cd "$WORK"
# gleam test runs the `app_test` entry (project name "app"); gleeunit then
# discovers every *_test function across all test modules. Only synthesize the
# entry if the task didn't ship its own (so we never clobber a real grader).
mkdir -p test
if [ ! -f test/app_test.gleam ]; then
  printf 'import gleeunit\n\npub fn main() {\n  gleeunit.main()\n}\n' > test/app_test.gleam
fi

set +e
out="$(gleam test 2>&1)"
rc=$?
set -e
printf '%s\n' "$out"

# If the failure is dependency resolution while offline, make it legible: it is a
# sandbox limitation, not a bug in the code under test.
if [ "$rc" -ne 0 ] && printf '%s' "$out" | grep -qiE 'resolv|hex\.pm|registry|dependenc|sending request'; then
  echo "kungfu: could not resolve dependencies under --network none. If this project needs hex packages beyond the cached stdlib+gleeunit, set docker.network to \"bridge\" in ~/.kungfu/config.json (trades sandbox isolation for network access), or pre-cache them in the image." >&2
fi
exit "$rc"
