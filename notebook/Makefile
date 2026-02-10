
# Default input parameters
docker ?= docker
image ?= public.ecr.aws/eodh/eodh-default-notebook
tag ?= python-3.12-2026.02.1
python_version := $(shell echo $(tag) | sed -n 's/python-\([0-9.]*\)-.*/\1/p')

.SILENT:
MAKEFLAGS += --no-print-directory

.PHONY: container-build
container-build:
	$(docker) build --build-arg PYTHON_VERSION=$(python_version) -t $(image):$(tag) .

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
		pytest /home/jovyan/tests -v
