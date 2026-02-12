"""Test that all required packages are importable.

Run with: pytest tests/test_imports.py -v
"""

import subprocess
import json
from importlib.metadata import version as get_package_version

import pytest


def _version_or_metadata(module, package_name: str) -> str:
    """Return __version__ from module, or version from package metadata."""
    v = getattr(module, "__version__", None)
    if v is not None:
        return v
    try:
        return get_package_version(package_name)
    except Exception:
        return "unknown"


class TestDataSciencePackages:
    """Test data science package imports."""

    def test_numpy(self):
        import numpy as np
        print(f"numpy: {np.__version__}", end=" ")
        assert np.__version__

    def test_scipy(self):
        import scipy
        print(f"scipy: {scipy.__version__}", end=" ")
        assert scipy.__version__

    def test_matplotlib(self):
        import matplotlib
        print(f"matplotlib: {matplotlib.__version__}", end=" ")
        assert matplotlib.__version__

    def test_pandas(self):
        import pandas as pd
        print(f"pandas: {pd.__version__}", end=" ")
        assert pd.__version__

    def test_scikit_image(self):
        import skimage
        print(f"scikit-image: {skimage.__version__}", end=" ")
        assert skimage.__version__

    def test_networkx(self):
        import networkx as nx
        print(f"networkx: {nx.__version__}", end=" ")
        assert nx.__version__

    def test_scikit_learn(self):
        import sklearn
        print(f"scikit-learn: {sklearn.__version__}", end=" ")
        assert sklearn.__version__

    def test_xarray(self):
        import xarray as xr
        print(f"xarray: {xr.__version__}", end=" ")
        assert xr.__version__

    def test_zarr(self):
        import zarr
        print(f"zarr: {zarr.__version__}", end=" ")
        assert zarr.__version__

    def test_ipython(self):
        import IPython
        print(f"IPython: {IPython.__version__}", end=" ")
        assert IPython.__version__


class TestGeospatialPackages:
    """Test geospatial package imports."""

    def test_gdal(self):
        from osgeo import gdal
        print(f"GDAL: {gdal.VersionInfo()}", end=" ")
        assert gdal.VersionInfo()

    def test_rasterio(self):
        import rasterio
        print(f"rasterio: {rasterio.__version__}", end=" ")
        assert rasterio.__version__

    def test_geopandas(self):
        import geopandas as gpd
        print(f"geopandas: {gpd.__version__}", end=" ")
        assert gpd.__version__

    def test_pyproj(self):
        import pyproj
        print(f"pyproj: {pyproj.__version__}", end=" ")
        assert pyproj.__version__

    def test_shapely(self):
        import shapely
        print(f"shapely: {shapely.__version__}", end=" ")
        assert shapely.__version__


class TestAWSPackages:
    """Test AWS package imports."""

    def test_boto3(self):
        import boto3
        print(f"boto3: {boto3.__version__}", end=" ")
        assert boto3.__version__

    def test_botocore(self):
        import botocore
        print(f"botocore: {botocore.__version__}", end=" ")
        assert botocore.__version__

    def test_s3fs(self):
        import s3fs
        print(f"s3fs: {s3fs.__version__}", end=" ")
        assert s3fs.__version__


class TestEODHPackages:
    """Test EODH platform package imports."""

    def test_pyeodh(self):
        import pyeodh
        print(f"pyeodh: {pyeodh.__version__}", end=" ")
        assert pyeodh.__version__

    def test_s3contents(self):
        import s3contents
        v = _version_or_metadata(s3contents, "s3contents")
        print(f"s3contents: {v}", end=" ")

    def test_hybridcontents(self):
        import hybridcontents
        v = _version_or_metadata(hybridcontents, "hybridcontents")
        print(f"hybridcontents: {v}", end=" ")


class TestDaskAndWidgets:
    """Test dask-kubernetes and ipywidgets package imports."""

    def test_dask_kubernetes(self):
        import dask_kubernetes
        print(f"dask-kubernetes: {dask_kubernetes.__version__}", end=" ")
        assert dask_kubernetes.__version__

    def test_ipywidgets(self):
        import ipywidgets
        print(f"ipywidgets: {ipywidgets.__version__}", end=" ")
        assert ipywidgets.__version__


class TestKernels:
    """Test that Jupyter kernels are available."""

    def test_python_kernel(self):
        import sys
        print(f"Python: {sys.version.split()[0]}", end=" ")
        result = subprocess.run(
            ["jupyter", "kernelspec", "list", "--json"],
            capture_output=True,
            text=True,
        )
        kernels = json.loads(result.stdout)
        assert "python3" in kernels["kernelspecs"]

    def test_r_kernel(self):
        result = subprocess.run(
            ["jupyter", "kernelspec", "list", "--json"],
            capture_output=True,
            text=True,
        )
        kernels = json.loads(result.stdout)
        assert "ir" in kernels["kernelspecs"]
        r_version_result = subprocess.run(
            ["Rscript", "-e", "cat(R.version.string)"],
            capture_output=True,
            text=True,
        )
        if r_version_result.returncode == 0:
            print(f"R: {r_version_result.stdout.strip()}", end="")
        else:
            print("R: (could not determine)", end=" ")

    def test_julia_kernel(self):
        result = subprocess.run(
            ["jupyter", "kernelspec", "list", "--json"],
            capture_output=True,
            text=True,
        )
        kernels = json.loads(result.stdout)
        # Julia kernel name may vary
        julia_kernels = [k for k in kernels["kernelspecs"] if "julia" in k.lower()]
        assert len(julia_kernels) > 0, "No Julia kernel found"
        julia_version_result = subprocess.run(
            ["julia", "--version"],
            capture_output=True,
            text=True,
        )
        if julia_version_result.returncode == 0:
            version_out = (julia_version_result.stdout or julia_version_result.stderr or "").strip()
            print(f"Julia: {version_out}", end=" ")
        else:
            print("Julia: (could not determine)", end=" ")


class TestGDALDrivers:
    """Test that required GDAL drivers are available."""

    def test_required_drivers(self):
        """Test essential GDAL drivers are available."""
        from osgeo import gdal
        required_drivers = ["GTiff", "COG", "VRT"]
        missing = []
        for driver in required_drivers:
            if gdal.GetDriverByName(driver) is None:
                missing.append(driver)
        assert not missing, f"Missing GDAL drivers: {missing}"


class TestWorkflows:
    """Test typical user workflows."""

    def test_geopandas_crs(self):
        """Test CRS operations with geopandas."""
        import geopandas as gpd
        from shapely.geometry import Point

        gdf = gpd.GeoDataFrame({"geometry": [Point(0, 0)]}, crs="EPSG:4326")
        assert gdf.crs.to_epsg() == 4326

        # Test reprojection
        gdf_utm = gdf.to_crs("EPSG:32631")
        assert gdf_utm.crs.to_epsg() == 32631

    def test_xarray_creation(self):
        """Test xarray DataArray creation."""
        import xarray as xr
        import numpy as np

        da = xr.DataArray(
            np.random.rand(10, 10),
            dims=["x", "y"],
            coords={"x": range(10), "y": range(10)},
        )
        assert da.shape == (10, 10)
        assert "x" in da.dims
        assert "y" in da.dims

    def test_rasterio_memfile(self):
        """Test rasterio memory file operations."""
        import rasterio
        from rasterio.io import MemoryFile
        import numpy as np

        data = np.random.randint(0, 255, (1, 100, 100), dtype=np.uint8)

        with MemoryFile() as memfile:
            with memfile.open(
                driver="GTiff",
                height=100,
                width=100,
                count=1,
                dtype=data.dtype,
                crs="EPSG:4326",
            ) as dst:
                dst.write(data)

            with memfile.open() as src:
                assert src.crs.to_epsg() == 4326
                assert src.shape == (100, 100)
