FROM quay.io/jupyter/base-notebook:python-3.12 AS build-stage

USER root

RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | sh -
RUN apt-get install -y nodejs

USER ${NB_UID}

RUN python -m pip install --upgrade pip
RUN python -m pip install jupyter-fs==1.0.1

RUN jupyter server extension enable jupyter_fs --sys-prefix
RUN jupyter lab extension enable @jupyterlab/jupyter-fs
RUN jupyter lab build --dev-build=False --minimize=False


FROM quay.io/jupyter/base-notebook:python-3.12

USER root

RUN apt-get update && apt-get install -y curl git nano unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip awscliv2.zip \
  && ./aws/install \
  && rm -rf awscliv2.zip aws

COPY --from=build-stage /opt/conda /opt/conda

USER ${NB_UID}

RUN python -m pip install --upgrade pip
RUN python -m pip install boto3==1.37.20 pyeodh==0.1.2 shapely==2.0.7 \
  geopandas==1.0.1 python-dotenv==1.0.1
