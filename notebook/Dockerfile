ARG PYTHON_VERSION
FROM quay.io/jupyter/datascience-notebook:python-${PYTHON_VERSION}

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

# Cleanup
RUN rm -f /tmp/environment.yml /tmp/requirements.txt
