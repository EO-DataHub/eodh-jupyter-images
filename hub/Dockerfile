FROM quay.io/jupyterhub/k8s-hub:4.3.2

# The base image ships pre-October 2026 ca-certificates (eMudhra distrust) and libbrotli1 (CVE-2026-111497)
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends --only-upgrade ca-certificates libbrotli1 \
 && rm -rf /var/lib/apt/lists/*
USER jovyan

RUN python3 -m pip install --no-cache-dir boto3==1.37.20 eodh-jpyauth==0.1.6 certifi==2026.10.23

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
