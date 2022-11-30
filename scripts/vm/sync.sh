#!/usr/bin/env bash

# Follow README.md to install

# Check if env vars set
if [[ -z "${PACKAGE_DIR}" ]]
then
    echo "PACKAGE_DIR env var is not set"
    exit 1
fi

if [[ -z "${GH_ACCESS_TOKEN}" ]]
then
    echo "GH_ACCESS_TOKEN env var is not set"
    exit 1
fi

if [[ -z "${API_PORT}" ]]
then
    echo "API_PORT env var is not set"
    exit 1
fi

build_lavi () {
    GOOS=$1 GOARCH=$2 go build -o lavi-cli-$1-$2
    if [[ $1 = "darwin" || $1 = "linux" ]]
    then
        chmod +x lavi-cli-$1-$2
    fi

    mkdir "$PACKAGE_DIR/lavi-cli-$1-$2"
    mv lavi-cli-$1-$2 "$PACKAGE_DIR/lavi-cli-$1-$2"
    cp INSTALL.txt "$PACKAGE_DIR/lavi-cli-$1-$2"

    if [[ $1 = "windows" ]]
    then
        mv lavi-cli-$1-$2 lavi-cli-$1-$2.exe
    fi
    zip -r "$PACKAGE_DIR/downloads/lavi/lavi-cli-$1-$2.zip" "$PACKAGE_DIR/lavi-cli-$1-$2"
    rm -rf "$PACKAGE_DIR/lavi-cli-$1-$2"
}

cd "$PACKAGE_DIR" || exit 1

sudo git pull

echo "building archives"

cd "$PACKAGE_DIR/lavi-cli" || exit 1

mkdir "$PACKAGE_DIR/downloads/lavi" -p

build_lavi darwin amd64
build_lavi darwin arm64

build_lavi linux amd64
build_lavi linux arm64

build_lavi windows amd64

cd "$PACKAGE_DIR" || exit 1

sudo --preserve-env docker compose build
sudo --preserve-env docker compose up -d
