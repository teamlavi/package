#!/usr/bin/env bash

# Follow README.md to install

# Check if env var set
if [[ -z "${PACKAGE_DIR}" ]]
then
    echo "PACKAGE_DIR env var is not set"
    exit 1
fi

cd "$PACKAGE_DIR" || exit 1

sudo docker compose build
sudo docker compose up -d
