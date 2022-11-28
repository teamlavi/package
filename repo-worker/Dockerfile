# Builder image
FROM python:3.10-slim as builder

RUN apt-get update -y
RUN apt-get install -y gcc

RUN python3 -m pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade --user -r /requirements.txt


# Main image
FROM python:3.10-slim as main
LABEL org.opencontainers.image.authors="Levi Lutz (contact.levilutz@gmail.com)"

RUN apt-get update -y
RUN apt-get install -y npm curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs
RUN apt-get clean -y

# Gotta install poetry for lavi poetry command
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to end of PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy lavi binary to image
COPY bin/lavi /usr/local/bin
RUN chmod +x /usr/local/bin/lavi

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=$PYTHONPATH:/src

COPY repo_worker /src/repo_worker
COPY tests /src/tests

WORKDIR /src
CMD ["echo", "No cmd provided"]
