# Gleam verification sandbox.
#
# Bump this tag to the current Gleam release:
#   https://github.com/gleam-lang/gleam/pkgs/container/gleam
FROM ghcr.io/gleam-lang/gleam:v1.15.0-erlang-alpine

# Non-root user for defense in depth.
RUN adduser -D -h /home/kungfu kungfu

# Warm the hex dependency cache OFFLINE-FIRST: build a template project so
# gleam_stdlib + gleeunit are compiled into the image. verify.sh seeds each task
# from this template so `gleam build`/`gleam test` works with --network none.
# Bench tasks must use the same deps this template generates (stdlib + gleeunit).
RUN mkdir -p /opt && cd /opt && gleam new app --skip-git && cd app && gleam test
RUN chown -R kungfu:kungfu /opt

COPY verify.sh /usr/local/bin/verify.sh
RUN chmod +x /usr/local/bin/verify.sh

USER kungfu
WORKDIR /home/kungfu
ENTRYPOINT ["/usr/local/bin/verify.sh"]
