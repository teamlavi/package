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
    sudo mkdir -p "$PACKAGE_DIR/lavi-cli/ui/build" 
    GOOS=$1 GOARCH=$2 /usr/local/go/bin/go build -o lavi-cli-$1-$2
    if [[ $1 = "darwin" || $1 = "linux" ]]
    then
        sudo chmod +x lavi-cli-$1-$2
    fi

    sudo mkdir "$PACKAGE_DIR/lavi-cli-$1-$2"
    sudo mv lavi-cli-$1-$2 "$PACKAGE_DIR/lavi-cli-$1-$2"
    sudo cp INSTALL.txt "$PACKAGE_DIR/lavi-cli-$1-$2"

    if [[ $1 = "windows" ]]
    then
        sudo mv lavi-cli-$1-$2 lavi-cli-$1-$2.exe
    fi
    sudo zip -r "$PACKAGE_DIR/downloads/lavi/lavi-cli-$1-$2.zip" "$PACKAGE_DIR/lavi-cli-$1-$2"
    sudo rm -rf "$PACKAGE_DIR/lavi-cli-$1-$2"
}

build_lava () {
    GOOS=$1 GOARCH=$2 /usr/local/go/bin/go build -o lava-cli-$1-$2
    if [[ $1 = "darwin" || $1 = "linux" ]]
    then
        sudo chmod +x lava-cli-$1-$2
    fi

    sudo mkdir "$PACKAGE_DIR/lava-cli-$1-$2"
    sudo mv lava-cli-$1-$2 "$PACKAGE_DIR/lava-cli-$1-$2"
    sudo cp INSTALL.txt "$PACKAGE_DIR/lava-cli-$1-$2"

    if [[ $1 = "windows" ]]
    then
        sudo mv lava-cli-$1-$2 lava-cli-$1-$2.exe
    fi
    sudo zip -r "$PACKAGE_DIR/downloads/lava/lava-cli-$1-$2.zip" "$PACKAGE_DIR/lava-cli-$1-$2"
    sudo rm -rf "$PACKAGE_DIR/lava-cli-$1-$2"
}

cd "$PACKAGE_DIR" || exit 1

sudo git pull

echo "building lavi archives"

mkdir "$PACKAGE_DIR/downloads/lavi" -p
mkdir "$PACKAGE_DIR/downloads/lava" -p

cd "$PACKAGE_DIR/lavi-cli" || exit 1

build_lavi darwin amd64
build_lavi darwin arm64

build_lavi linux amd64
build_lavi linux arm64

build_lavi windows amd64

cd "$PACKAGE_DIR/lava-cli" || exit 1

build_lava darwin amd64
build_lava darwin arm64

build_lava linux amd64
build_lava linux arm64

build_lava windows amd64

cd "$PACKAGE_DIR" || exit 1

sudo --preserve-env docker compose build
sudo --preserve-env docker compose up -d
