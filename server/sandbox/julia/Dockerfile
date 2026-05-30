# Julia verification sandbox.
# Bump the tag as new releases land: https://hub.docker.com/_/julia
FROM julia:1.11

RUN useradd -m kungfu
COPY verify.sh /usr/local/bin/verify.sh
RUN chmod +x /usr/local/bin/verify.sh

USER kungfu
WORKDIR /home/kungfu
ENTRYPOINT ["/usr/local/bin/verify.sh"]
