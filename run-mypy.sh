#!/usr/bin/env bash
# Script used during pre-commit to ensure correct execution of mypy.
set -o errexit
# Change directory to the project root directory.
cd "$(dirname "$0")"
# Ignore auto-generated file
sed -i "1s/.*/# type: ignore/" resources_rc.py
# Run mypy using the config file
mypy . --config-file mypy.ini