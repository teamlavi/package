#!/usr/bin/env bash
# Expects to be run from code root (.../container in repo, /src in container)

set -e

# export MYPYPATH=stubs

mypy . --strict --exclude=tests
black --check --diff .
flake8 --max-line-length=88 .
