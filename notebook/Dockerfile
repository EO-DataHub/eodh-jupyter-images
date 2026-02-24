ARG PYTHON_VERSION
FROM quay.io/jupyter/datascience-notebook:python-${PYTHON_VERSION} AS base

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    nano \
    unzip \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

USER ${NB_UID}

# Install geospatial packages via mamba (binary compatibility)
ARG PYTHON_VERSION
COPY python-${PYTHON_VERSION}/environment.yml /tmp/environment.yml
RUN mamba env update -n base -f /tmp/environment.yml && mamba clean --all -f -y

# Install Python packages via pip (pinned versions)
COPY python-${PYTHON_VERSION}/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy Jupyter configuration
COPY jupyter_server_config.py /etc/jupyter/jupyter_server_config.py

# -----------------------------------------------------------------------------
# CUDA stage: only built when using --target cuda (e.g. make container-build-cuda)
# Adds full CUDA 12 runtime + torch + CuPy. Base stage has no CUDA layers.
# -----------------------------------------------------------------------------
FROM base AS cuda
ARG PYTHON_VERSION
COPY python-${PYTHON_VERSION}/requirements-cuda.txt /tmp/requirements-cuda.txt
USER root
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && \
    dpkg -i cuda-keyring_1.1-1_all.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends cuda-runtime-12-4 && \
    rm -rf /var/lib/apt/lists/* cuda-keyring_1.1-1_all.deb
ENV CUDA_PATH=/usr/local/cuda-12.4
USER ${NB_UID}
RUN pip install --no-cache-dir -r /tmp/requirements-cuda.txt
