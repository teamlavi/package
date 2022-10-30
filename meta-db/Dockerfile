# Builder image
FROM python:3.10-slim as builder

RUN python3 -m pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade --user -r /requirements.txt


# Main image
FROM python:3.10-slim as main
LABEL org.opencontainers.image.authors="Levi Lutz (contact.levilutz@gmail.com)"

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=$PYTHONPATH:/src

COPY meta_db /src/meta_db
COPY tests /src/tests

WORKDIR /src
CMD ["echo", "No cmd provided"]
