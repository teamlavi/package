FROM golang:1.18 as GO
WORKDIR /dep-tree-gen 
COPY dep-tree-gen .
WORKDIR /app
COPY lavi-cli .

# need this so go doesnt freak out
RUN mkdir ui/build
RUN echo "<p>empty</p>" >> ui/build/index.html

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o lavi .
RUN cp lavi /usr/local/bin
# Gotta install python and npm
RUN apt-get install python3 curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
 apt-get install -y nodejs

CMD ["echo", "No cmd provided"]