# build ui first
FROM node:16.13.0-slim as UI

WORKDIR /app
COPY lavi-cli .

WORKDIR /app/ui
RUN npm i
RUN npm run build

# build cli
FROM golang:1.18 as GO
WORKDIR /dep-tree-gen 
COPY dep-tree-gen .
WORKDIR /app
COPY --from=UI /app ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o lavi .
RUN cp lavi /usr/local/bin
# Gotta install python and npm
RUN apt-get install python3 curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
 apt-get install -y nodejs

CMD ["echo", "No cmd provided"]