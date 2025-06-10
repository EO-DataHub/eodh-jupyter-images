FROM quay.io/jupyter/base-notebook:python-3.12

USER root

RUN apt-get update && apt-get install -y curl git nano unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip awscliv2.zip \
  && ./aws/install \
  && rm -rf awscliv2.zip aws

USER ${NB_UID}

RUN python -m pip install --upgrade jupyterlab==4.4.0 jupyterlab-git==0.51.1
RUN python -m pip install boto3==1.37.1 pyeodh==0.1.4 shapely==2.0.7 \
  geopandas==1.0.1 python-dotenv==1.0.1 s3contents==0.11.2 hybridcontents==0.4.0

COPY jupyter_server_config.py /etc/jupyter/jupyter_server_config.py
