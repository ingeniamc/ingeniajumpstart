#!/usr/bin/env bash
set -o errexit
# Change directory to the project root directory.
cd "$(dirname "$0")"
# Run mypy using the config file
mypy . --config-file mypy.ini