#!/usr/bin/env bash
# Expects to be run from code root (.../container in repo, /src in container)

set -e

mypy lavi_worker --strict
black --check --diff lavi_worker
flake8 --max-line-length=88 lavi_worker

# No mypy for tests (gets messy with patching / mocking sometimes)
black --check --diff tests
flake8 --max-line-length=88 tests
