# EO DataHub Default Notebook

The default EO DataHub user notebook server based on [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-datascience-notebook) `datascience-notebook`.

## Features

- **Multi-language**: Python, R, and Julia kernels
- **Geospatial**: GDAL, rasterio, geopandas, pyproj, shapely
- **Data Science**: numpy, scipy, pandas, matplotlib, scikit-learn, xarray, zarr
- **AWS Integration**: boto3, s3fs, AWS CLI
- **EODH Platform**: pyeodh, s3contents, hybridcontents

## Supported Python Versions

| Python | Status | Base Image Tag |
|--------|--------|----------------|
| 3.12 | Supported | `python-3.12-2026.02` |
| 3.13 | Supported | `python-3.13-2026.02` |

## Building

### Using `make` command

The Makefile derives the Python version from the image tag (e.g. `python-3.12-2026.02` → `3.12`).

```bash
# Build with a specific tag (Python version is extracted from the tag)
make container-build tag=python-3.12-2026.02.1

# Build and push to ECR
make publish tag=python-3.13-2026.02.1

# Override image repository
make container-build image=public.ecr.aws/eodh/my-notebook tag=python-3.13-2026.02.1

# Run tests
make test tag=python-3.12-2026.02.1
```

### Make Targets

| Target | Description |
|--------|-------------|
| `make container-build` | Build the image |
| `make container-push` | Push image to ECR |
| `make publish` | Build and push |
| `make test` | Run pytest in container (mounts `tests/`) |

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `docker` | `docker` | Docker CLI to use |
| `image` | `public.ecr.aws/eodh/eodh-default-notebook` | Image repository |
| `tag` | `python-3.xx-2026.02` | Full image tag; Python version is derived from it |

## Release Process

### Versioning

Images use **CalVer** tagging: `python-<VERSION>-<YYYY>.<MM>[.<PATCH>]`

| Tag | Meaning |
|-----|---------|
| `python-3.13-2026.02` | Regular release |
| `python-3.13-2026.02.3` | Patch release (security fix, hotfix) |

### Regular Release

1. Update dependencies in `python-X.XX/requirements.txt` and `environment.yml`
2. Run tests locally: `make test tag=python-3.13-2026.02`
3. Build and push:
   ```bash
   make publish tag=python-3.13-2026.02
   ```
4. Tag the commit:
   ```bash
   git tag default-python-3.13-2026.02
   git push origin --tags
   ```
5. Update JupyterHub configuration to use new image tag

### Patch Release

For security fixes or critical bugs on an existing release, use a tag with a patch suffix:

```bash
make publish tag=python-3.13-2026.02
```

### Adding a New Python Version

When a new Python version is released (typically October each year):

1. Create new dependency folder:
   ```bash
   mkdir python-3.14
   cp python-3.13/requirements.txt python-3.14/
   cp python-3.13/environment.yml python-3.14/
   ```
2. Update pinned versions for Python 3.14 compatibility
3. Verify base image exists: `quay.io/jupyter/datascience-notebook:python-3.14`
4. Build and test: `make container-build tag=python-3.14-2026.10.01 && make test tag=python-3.14-2026.10.01`
5. Update this README's "Supported Python Versions" table
6. Add to JupyterHub profile list

### Deprecating a Python Version

Following [SPEC-0000](https://scientific-python.org/specs/spec-0000/), Python versions are supported for 3 years from release.

**Timeline:**

| Phase | Timing | Action |
|-------|--------|--------|
| **Supported** | Until 3 months before drop date | Normal releases |
| **Deprecated** | 3 months before drop date | Add deprecation notice, warn users |
| **Sunset** | At drop date | Stop publishing new images |
| **EOL** | 1 month after drop date | Remove from JupyterHub profiles |

**Deprecation Steps:**

1. Update "Supported Python Versions" table:
   ```
   | 3.11 | Deprecated (EOL: Oct 2025) | `python-3.11` |
   ```
2. Notify users via release notes and platform announcements
3. At sunset date, stop building new images for that version
4. At EOL date:
   - Remove `python-X.XX/` folder
   - Remove from JupyterHub profile list
   - Keep old images in ECR for users who pinned versions

### Release Checklist

- [ ] Dependencies updated and pinned
- [ ] Tests pass: `make test tag=python-X.XX-YYYY.MM`
- [ ] SPEC-0000 compliance verified
- [ ] Image built and pushed to ECR
- [ ] Git tag created and pushed
- [ ] JupyterHub configuration updated
- [ ] Release notes published (if applicable)

## Directory Structure

```
notebook/
├── Dockerfile                  # Multi-version build file
├── python-3.12/
│   ├── environment.yml         # Mamba dependencies (geospatial)
│   └── requirements.txt        # Pip dependencies (pinned versions)
├── python-3.13/
│   ├── environment.yml
│   └── requirements.txt
├── scripts/
│   └── validate_spec0000.py    # SPEC-0000 compliance validation
├── tests/
│   └── test_imports.py         # Package import tests
└── jupyter_server_config.py    # Jupyter server configuration
```

## Dependencies

Dependencies are split between mamba (conda-forge) and pip:

| Tool | Packages | Why |
|------|----------|-----|
| **mamba** | gdal, rasterio, pyproj | Binary compatibility for geospatial stack |
| **pip** | Everything else | Faster, more up-to-date versions |

Each Python version has its own pinned dependency files for reproducible builds.

## File Managers

The notebook uses HybridContentsManager to support both:
- Local filesystem (mounted Kubernetes volumes)
- AWS S3 buckets via s3contents

Configuration is in `jupyter_server_config.py`.

## Testing

```bash
# Run tests via make (uses current image:tag; mounts tests/ into container)
make test tag=python-3.13-2026.02.15

# Run tests with custom image
make test image=public.ecr.aws/eodh/eodh-default-notebook tag=python-3.13-2026.02
```

## SPEC-0000 Compliance

This image follows [Scientific Python SPEC-0000](https://scientific-python.org/specs/spec-0000/):

- Python: 3-year support window from release
- Core packages: 2-year support window from release

The `validate_spec0000.py` script checks compliance during builds.
