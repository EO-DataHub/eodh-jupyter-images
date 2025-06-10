# EO DataHub Jupyter Notebook Images

A collection of images for the UK EO DataHub Jupyter Hub.

Each image is located in its own directory. A Dockerfile and Makefile is defined for each image.

To build and push the Jupyter images in this repository, first update the image tag in the Makefile and run the following commands

```bash
# build and push default image
cd default
make container-build
make container-push

# build and push hub image
cd hub
make container-build
make container-push
```