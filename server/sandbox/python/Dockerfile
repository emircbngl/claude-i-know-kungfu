# Python verification sandbox (demonstrates the language-agnostic learn loop on
# a language Claude already knows well).
FROM python:3.12-slim

RUN useradd -m kungfu
RUN pip install --no-cache-dir pytest

COPY verify.sh /usr/local/bin/verify.sh
RUN chmod +x /usr/local/bin/verify.sh

USER kungfu
WORKDIR /home/kungfu
ENTRYPOINT ["/usr/local/bin/verify.sh"]
