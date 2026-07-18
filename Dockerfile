
FROM python:3.12

# Use .dockerignore to exclude unnecessary files (e.g. .git, tests, docs, assets, etc.)

# Copy only requirements.txt and main files to root
COPY requirements.txt ./

# Copy only necessary source files to /src
COPY src/ /src/

WORKDIR /src

# RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

# Pinned build-tooling versions keep the image reproducible; override with
# --build-arg if a newer patched release is needed. These pins clear the
# pip / setuptools / wheel CVE scan findings (setuptools 83 also vendors the
# patched jaraco.context 6.1 + wheel 0.46.3 under setuptools/_vendor/).
ARG PIP_VERSION=26.1.2
ARG SETUPTOOLS_VERSION=83.0.0
ARG WHEEL_VERSION=0.47.0
# Upgrade build tooling & purge old bundled/cached wheels the base image ships
# (fixes pip / setuptools / wheel CVEs; ensurepip stashes vulnerable .whl files
# that scanners still flag even after an upgrade)
RUN pip install --no-cache-dir --upgrade "pip==${PIP_VERSION}" "setuptools==${SETUPTOOLS_VERSION}" "wheel==${WHEEL_VERSION}" \
    && { \
        find /usr/local/lib -type d -name "_bundled" -path "*ensurepip*" -exec rm -rf {} + 2>/dev/null; \
        rm -rf /root/.cache/pip; \
    }

RUN pip install --no-cache-dir -r /requirements.txt

RUN chmod 444 main.py
RUN chmod 444 /requirements.txt

ENV PORT 8085

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 900 main:app


# Run the application
# CMD ["python", "main.py"]