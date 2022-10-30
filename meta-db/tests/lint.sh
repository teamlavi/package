#!/usr/bin/env bash
# Expects to be run from code root (.../container in repo, /src in container)

set -e

mypy meta_db --strict
black --check --diff meta_db
flake8 --max-line-length=88 meta_db

# No mypy for tests (gets messy with patching / mocking sometimes)
black --check --diff tests
flake8 --max-line-length=88 tests
