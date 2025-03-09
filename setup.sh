#!/usr/bin/env bash
# encoding:utf-8

# Set up the libraries inside the docker container and self destructs in the end

# Exit upon error to preemptively detect incompatibilities at build stage
set -e
# Install the system libraries
apt-get --assume-yes update
# Set the timezone to avoid input prompt while installing libraries
ZONE="Asia/Singapore" # "UTC"
ln --symbolic --no-dereference --force /usr/share/zoneinfo/$ZONE /etc/localtime
echo $ZONE > /etc/timezone
uv venv "$ENV_DIR" # The last argument gives the directory name
# Install the python dependencies
time uv pip install --requirement requirements.txt

# Clean up to reduce image size
rm requirements.txt setup.sh