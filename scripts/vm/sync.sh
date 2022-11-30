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

build () {
    PREFIX=$1
    GOOS=$2
    GOARCH=$3

    FILE="$PREFIX-cli-$GOOS-$GOARCH"

    if [[ $PREFIX = "lavi" ]]
    then
        sudo mkdir -p "$PACKAGE_DIR/lavi-cli/ui/build" 
    fi
    GOOS=$GOOS GOARCH=$GOARCH /usr/local/go/bin/go build -o $PREFIX
    if [[ $GOOS = "darwin" || $GOOS = "linux" ]]
    then
        sudo chmod +x $PREFIX
    fi

    sudo mkdir $FILE
    sudo mv $PREFIX "$FILE/"
    sudo cp INSTALL.txt "$FILE/"

    if [[ $GOOS = "windows" ]]
    then
        sudo mv "$FILE/$PREFIX" "$FILE/$PREFIX.exe"
    fi
    
    sudo zip -r -j "$PACKAGE_DIR/downloads/$PREFIX/$FILE.zip" "$FILE/"
    sudo rm -rf "$FILE"
}

cd "$PACKAGE_DIR" || exit 1

sudo git pull

echo "building lavi archives"

rm -rf "$PACKAGE_DIR/downloads" || :

mkdir "$PACKAGE_DIR/downloads/lavi" -p
mkdir "$PACKAGE_DIR/downloads/lava" -p

cd "$PACKAGE_DIR/lavi-cli" || exit 1

build lavi darwin amd64
build lavi darwin arm64

build lavi linux amd64
build lavi linux arm64

build lavi windows amd64

cd "$PACKAGE_DIR/lava-cli" || exit 1

build lava darwin amd64
build lava darwin arm64

build lava linux amd64
build lava linux arm64

build lava windows amd64

cd "$PACKAGE_DIR" || exit 1

sudo --preserve-env docker compose build
sudo --preserve-env docker compose up -d
