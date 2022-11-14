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

# TODO Move these lines to builder
RUN apt-get update -y
RUN apt-get install -y npm
RUN apt-get clean -y

# Gotta install npm for lavi npm command
RUN apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
 apt-get install -y nodejs

# Copy lavi binary to image
COPY bin/lavi /usr/local/bin

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=$PYTHONPATH:/src

COPY repo_worker /src/repo_worker
COPY tests /src/tests

WORKDIR /src
CMD ["echo", "No cmd provided"]
