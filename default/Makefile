# Default input parameters
docker ?= docker
image ?= public.ecr.aws/eodh/eodh-default-notebook
version ?= python-3.12-0.2.11

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