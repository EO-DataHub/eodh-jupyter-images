
# Default input parameters
docker ?= docker
image ?= public.ecr.aws/eodh/eodh-default-notebook
tag ?= python-3.13-2026.02.0
python_version := $(shell echo $(tag) | sed -n 's/python-\([0-9.]*\)-.*/\1/p')


.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: container-build
container-build:
	$(docker) build --build-arg PYTHON_VERSION=$(python_version) -t $(image):$(tag) .

.PHONY: container-build-cuda
# CUDA image: use tag with -cuda suffix (e.g. tag=python-3.13-2026.02.0-cuda).
container-build-cuda:
	$(docker) build --platform linux/amd64 --build-arg PYTHON_VERSION=$(python_version) --build-arg BUILD_CUDA=1 -t $(image):$(tag) .

.PHONY: container-push
container-push:
	$(docker) push $(image):$(tag)

.PHONY: publish
publish: container-build container-push

.PHONY: test
test:
	@echo "Testing $(image):$(tag)"
	$(docker) run --rm \
		-v $(CURDIR)/tests:/home/jovyan/tests:ro \
		$(image):$(tag) \
		pytest /home/jovyan/tests -v -s

.PHONY: shell
shell:
	$(docker) run -it --rm $(image):$(tag) /bin/bash
