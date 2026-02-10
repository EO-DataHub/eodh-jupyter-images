# Default EO DataHub Notebook Server

This is the default EO DataHub user notebook server. It provides commonly used Python and EO packages, as well as some convenience applications.

## File Managers

In order to use both a local file handler (which can be mounted Kubernetes volume) and also mount a POSIX AWS S3 volume, it was necessary to use the HybridContentsManager JupyterHub plugin. This allows multiple FileHandlers to be used simultaneously.

The HybridContentsManager is configured in the ./jupyter_server_config.py file, which is copied into the container image on build.
