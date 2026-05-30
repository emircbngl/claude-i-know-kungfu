#!/bin/sh
# Julia verify: run test/runtests.jl if present (a failing @testset exits non-zero),
# else parse/compile-check every src file by including it. The Julia stdlib (incl.
# Test) is bundled in the image, so this works fully offline (--network none).
set -eu
WORK=/home/kungfu/work
rm -rf "$WORK"
mkdir -p "$WORK"
cp -a /src/. "$WORK"/ 2>/dev/null || cp -r /src/* "$WORK"/
cd "$WORK"

if [ -f test/runtests.jl ]; then
  exec julia --color=no --startup-file=no test/runtests.jl
fi

exec julia --color=no --startup-file=no -e 'for f in readdir("src", join=true); endswith(f, ".jl") && include(f); end'
