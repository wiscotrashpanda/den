# [Choice] Ubuntu base image: 22.04, 20.04, etc.
ARG VARIANT=ubuntu
FROM mcr.microsoft.com/devcontainers/base:0-${VARIANT}

# Install common tools and runtimes used by many CLIs
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
  && rm -rf /var/lib/apt/lists/*

# Ensure npm global installs are available to the vscode user
ENV NPM_CONFIG_PREFIX=/home/vscode/.npm-global
ENV PATH="$NPM_CONFIG_PREFIX/bin:$PATH"
RUN mkdir -p /home/vscode/.npm-global && chown -R vscode:vscode /home/vscode/.npm-global

# Copy install scripts
COPY .devcontainer/scripts /tmp/devcontainer-scripts
RUN chmod +x /tmp/devcontainer-scripts/install-opencode.sh

# Keep image size small
USER vscode
WORKDIR /workspace
