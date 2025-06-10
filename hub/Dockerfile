FROM quay.io/jupyterhub/k8s-hub:4.2.0

RUN python3 -m pip install --no-cache-dir boto3==1.37.20 eodh-jpyauth==0.1.3

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
