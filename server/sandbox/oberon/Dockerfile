# Oberon (Oberon-07) verification sandbox.
# No official image exists, so we build OBNC (Karl Landstrom's Oberon-07 compiler,
# https://miasap.se/obnc/) from source. OBNC compiles Oberon to C and invokes cc,
# so gcc + libgc stay in the image and are needed at verify time too.
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc libc6-dev libgc-dev make curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Build + install OBNC (tarball top dir is obnc-0.17.2).
RUN curl -sSL https://miasap.se/obnc/downloads/obnc_0.17.2.tar.gz -o /tmp/obnc.tar.gz \
    && cd /tmp && tar xzf obnc.tar.gz && cd obnc-0.17.2 \
    && ./build && ./install \
    && rm -rf /tmp/obnc*

RUN useradd -m kungfu
COPY verify.sh /usr/local/bin/verify.sh
RUN chmod +x /usr/local/bin/verify.sh

USER kungfu
WORKDIR /home/kungfu
ENTRYPOINT ["/usr/local/bin/verify.sh"]
