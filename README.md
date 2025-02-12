# EO DataHub Jupyter Notebook Images

A collection of images for the UK EO DataHub Jupyter Hub.

Each image is located in its own directory. A Dockerfile and Makefile is defined for each image.

```bash
# build and push default image
cd default
make container-build
make container-push
```