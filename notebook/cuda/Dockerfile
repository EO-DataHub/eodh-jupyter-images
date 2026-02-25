# CUDA image: build on top of the base image (build and tag base first).
ARG BASE_IMAGE=public.ecr.aws/eodh/eodh-default-notebook:python-3.13-2026.02.0
FROM ${BASE_IMAGE}

ARG PYTHON_VERSION
COPY requirements.txt /tmp/requirements.txt

USER root
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && \
    dpkg -i cuda-keyring_1.1-1_all.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends cuda-runtime-12-4 && \
    rm -rf /var/lib/apt/lists/* cuda-keyring_1.1-1_all.deb

ENV CUDA_PATH=/usr/local/cuda-12.4

USER ${NB_UID}
RUN pip install --no-cache-dir -r /tmp/requirements.txt
