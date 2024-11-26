#!/usr/bin/env bash

set -ex

uv run mypy xcdo
uv run ruff check xcdo tests examples
uv run ruff format --check xcdo tests examples
