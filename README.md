# EO DataHub Jupyter Notebook Images

A collection of images for the UK EO DataHub Jupyter Hub.

Each image is located in its own directory. A Dockerfile and Makefile is defined for each image.

```sh
# build and push default image
cd default
make container-build
make container-push
```

Remember to tag the commits that release images are built from. Use the tag format `<image-name>-<version>`, e.g. `default-python-3.12-0.2.11`.

```sh
git tag default-python-3.12-0.2.11
git push origin --tags
```
