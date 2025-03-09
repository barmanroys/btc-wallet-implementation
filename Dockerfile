# To build an image using this file
# IMAGE=btc-wallet-image
# $ time docker build --tag=btc-wallet-image ./
# This docker image has the uv package manager preinstalled
FROM ghcr.io/astral-sh/uv:debian
LABEL maintainer="Barman Roy, Swagato <swagatopablo@aol.com, +65 94668329>"
WORKDIR /app
# Copy the necessary scripts and files
COPY requirements.txt ./
COPY *.sh ./
COPY src/*.py src/
COPY data/seed.txt data/
# This environment variable represents the virtual
# environment directory to hold site packages
ENV ENV_DIR=".venv"
# Set up the container
RUN chmod +x *.sh && ./setup.sh
