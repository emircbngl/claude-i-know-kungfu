# Verification sandboxes

Each language has a Docker image that acts as the **truth oracle** for that
language. `kungfu_verify` runs generated code here; the compiler's verdict is
ground truth.

## The image contract

Every `sandbox/<lang>/` image must:

1. Expect the project source mounted **read-only at `/src`**.
2. Copy it to a writable workdir, then **build / type-check / test** it.
3. Print diagnostics to stdout/stderr and **exit non-zero on any failure**.
4. Run as a **non-root** user.

The server runs the image with `--network none`, CPU/memory/pids limits,
`--security-opt no-new-privileges`, and `--rm` (see `kungfu/verify.py`). All
language-specific logic lives here — adding a language never touches the server.

## Offline dependencies

Because verification runs with `--network none` by default, each image **warms
its dependency cache at build time** and `verify.sh` seeds every task from that
cache. If a task needs deps the image hasn't cached, either bake them into the
image or set `docker.network` to `"bridge"` in `~/.kungfu/config.json` (a
deliberate, documented trade-off against sandbox isolation).

## Adding a language

1. `mkdir sandbox/<lang>` with a `Dockerfile` + `verify.sh` honoring the contract.
2. Add the language + its file extensions to `managed_languages` in
   `~/.kungfu/config.json`.
3. `kungfu_verify` builds the image lazily on first use.

## Status

These Dockerfiles are written to the contract above but were **not built or run
in the authoring environment** (Docker was unavailable there). Validate them on a
Docker host before relying on the numbers; image base tags (e.g. the Gleam
release) may need bumping.
