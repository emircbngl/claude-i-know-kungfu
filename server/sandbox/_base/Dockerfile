# Reference base documenting the kungfu sandbox contract.
#
# Real language images use their own upstream toolchain base (see ../gleam,
# ../python). This image only demonstrates the contract and is handy for a
# language whose check is a single installed CLI. It is NOT used by default.

FROM alpine:3.20

RUN adduser -D -h /home/kungfu kungfu
COPY verify.sh /usr/local/bin/verify.sh
RUN chmod +x /usr/local/bin/verify.sh

USER kungfu
WORKDIR /home/kungfu
ENTRYPOINT ["/usr/local/bin/verify.sh"]
