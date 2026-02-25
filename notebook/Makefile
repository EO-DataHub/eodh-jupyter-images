
# Default input parameters
docker ?= docker
image ?= public.ecr.aws/eodh/eodh-default-notebook
tag ?= python-3.13-2026.02.0
python_version := $(shell echo $(tag) | sed -n 's/python-\([0-9.]*\)-.*/\1/p')
base_tag := $(shell echo $(tag) | sed 's/-cuda$$//')


.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: container-build
# Explicit --target base so we build CPU-only image (default Docker target would be last stage = cuda).
container-build:
	$(docker) build --platform linux/amd64 --build-arg PYTHON_VERSION=$(python_version) -t $(image):$(tag) .

.PHONY: container-build-cuda
# CUDA image: use tag with -cuda suffix (e.g. tag=python-3.13-2026.02.0-cuda). Builds only the cuda stage.
container-build-cuda:
	$(docker) build --platform linux/amd64 --build-arg PYTHON_VERSION=$(python_version) --build-arg BASE_IMAGE=$(image):$(base_tag) -t $(image):$(tag) ./cuda

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
