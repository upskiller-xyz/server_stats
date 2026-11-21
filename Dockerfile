# Stats image on Project Hummingbird (Red Hat hardened, distroless Python).
#
# Two stages: the -builder image (has pip and a shell) builds a venv, and the
# distroless runtime image (no shell, no package manager, runs as UID 65532)
# only receives the venv and the source. Both are pinned by index digest
# (multi-arch); Dependabot bumps them, or bump tag and digest together:
#   docker buildx imagetools inspect registry.access.redhat.com/hi/python:3.14
#
# No OS packages are installed: the opencv-python-headless and numpy wheels
# bundle their native libraries.

FROM registry.access.redhat.com/hi/python:3.15-builder@sha256:f0f26eaca78fb6e4a489640ab7578ea1022120ed044f31f575961f9935d102a9 AS build

# The builder image runs as 65532 too; installing into /opt needs root.
USER 0
RUN python3 -m venv /opt/venv
COPY requirements.txt /tmp/requirements.txt
# pip is only needed to build the venv; removing it keeps it (and its CVEs)
# out of the runtime image.
RUN /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt \
    && /opt/venv/bin/pip uninstall -y pip

FROM registry.access.redhat.com/hi/python:3.15@sha256:0766d2d64024695dc2cb90d251c247b834d5ea8b3dec28134f09e47ff6ad68a0

COPY --from=build /opt/venv /opt/venv
# Copied as root-owned files, so the runtime user cannot modify them; the
# service never writes to disk.
COPY requirements.txt /requirements.txt
COPY src/ /src/

WORKDIR /src

# PORT is read by gunicorn itself (no --bind: it binds 0.0.0.0:$PORT), so the
# platform can still override it without a shell to expand $PORT.
ENV PATH=/opt/venv/bin:$PATH \
    PORT=8085 \
    PYTHONUNBUFFERED=1

# The image default (65532), stated explicitly so a base-image change cannot
# silently make the service run as root.
USER 65532

EXPOSE 8085
CMD ["gunicorn", "--workers", "1", "--threads", "8", "--timeout", "900", "main:app"]
