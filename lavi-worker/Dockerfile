# Builder image
FROM python:3.10-slim as builder

RUN python3 -m pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade --user -r /requirements.txt


# Main image
# BASE_IMAGE_VERSION provided as garden output
ARG BASE_IMAGE_VERSION
FROM ${PROTOBUF_BASE_IMAGE_REPO}protobuf-base:${PROTOBUF_BASE_IMAGE_VERSION} as protobuf-base
FROM python:3.10-slim as main
LABEL org.opencontainers.image.authors="Levi Lutz (contact.levilutz@gmail.com)"

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=$PYTHONPATH:/src

COPY lavi_worker /src/lavi_worker
COPY tests /src/tests
COPY --from=protobuf-base /protobuf /src/protobuf

WORKDIR /src
CMD ["echo", "No cmd provided"]
