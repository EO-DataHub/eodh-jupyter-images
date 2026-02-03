# Default input parameters
DOCKER ?= docker
IMAGE ?= public.ecr.aws/eodh/eodh-default-notebook
PYTHON_VERSION ?= 3.13
PATCH ?=

# Generate CalVer tag: python-{VERSION}-{YYYY}.{MM}.{DD}[.{PATCH}]
DATE := $(shell date +%Y.%m.%d)
ifdef PATCH
TAG := python-$(PYTHON_VERSION)-$(DATE).$(PATCH)
else
TAG := python-$(PYTHON_VERSION)-$(DATE)
endif

.SILENT:
MAKEFLAGS += --no-print-directory

# Build the notebook image
#
# Usage:
#   make build                              # Build Python 3.13 (default)
#   make build PYTHON_VERSION=3.12          # Build Python 3.12
#   make build PYTHON_VERSION=3.14 PATCH=1  # Build Python 3.14 with patch
#
.PHONY: build
build:
	@echo "Building $(IMAGE):$(TAG)"
	$(DOCKER) build \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		-t $(IMAGE):$(TAG) \
		.

.PHONY: push
push:
	@echo "Pushing $(IMAGE):$(TAG)"
	$(DOCKER) push $(IMAGE):$(TAG)

.PHONY: publish
publish: build push

.PHONY: test
test:
	@echo "Testing $(IMAGE):$(TAG)"
	$(DOCKER) run --rm $(IMAGE):$(TAG) \
		python -c "import numpy, scipy, pandas; from osgeo import gdal; print('OK')"

.PHONY: info
info:
	@echo "IMAGE:          $(IMAGE)"
	@echo "PYTHON_VERSION: $(PYTHON_VERSION)"
	@echo "DATE:           $(DATE)"
	@echo "PATCH:          $(PATCH)"
	@echo "TAG:            $(TAG)"
