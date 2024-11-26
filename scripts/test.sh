#!/usr/bin/env bash

set -ex

# export PATH=${PATH}:$(pwd)/.conda_env/bin
export CDO=$(pwd)/.conda_env/bin/cdo
uv run pytest --cov --cov-report=term ${@}
