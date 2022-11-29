#!/usr/bin/env bash

# Follow README.md to install

# Check if env var set
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

cd "$PACKAGE_DIR" || exit 1

sudo git pull

sudo --preserve-env docker compose build
sudo --preserve-env docker compose up -d
