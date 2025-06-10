# Default input parameters
docker ?= docker
image ?= public.ecr.aws/eodh/eodh-jupyter-hub
version ?= 4.2.0-0.1.0

.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: container-build
container-build:
	$(docker) build -t $(image):$(version) .

.PHONY: container-push
container-push:
	$(docker) push $(image):$(version)

.PHONY: publish
publish: container-build container-push