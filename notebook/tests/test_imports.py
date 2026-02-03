"""Test that all required packages are importable.

Run with: pytest tests/test_imports.py -v
"""

import subprocess
import json

import pytest


class TestDataSciencePackages:
    """Test data science package imports."""

    def test_numpy(self):
        import numpy as np
        assert np.__version__

    def test_scipy(self):
        import scipy
        assert scipy.__version__

    def test_matplotlib(self):
        import matplotlib
        assert matplotlib.__version__

    def test_pandas(self):
        import pandas as pd
        assert pd.__version__

    def test_scikit_image(self):
        import skimage
        assert skimage.__version__

    def test_networkx(self):
        import networkx as nx
        assert nx.__version__

    def test_scikit_learn(self):
        import sklearn
        assert sklearn.__version__

    def test_xarray(self):
        import xarray as xr
        assert xr.__version__

    def test_zarr(self):
        import zarr
        assert zarr.__version__

    def test_ipython(self):
        import IPython
        assert IPython.__version__


class TestGeospatialPackages:
    """Test geospatial package imports."""

    def test_gdal(self):
        from osgeo import gdal
        assert gdal.VersionInfo()

    def test_rasterio(self):
        import rasterio
        assert rasterio.__version__

    def test_geopandas(self):
        import geopandas as gpd
        assert gpd.__version__

    def test_pyproj(self):
        import pyproj
        assert pyproj.__version__

    def test_shapely(self):
        import shapely
        assert shapely.__version__


class TestAWSPackages:
    """Test AWS package imports."""

    def test_boto3(self):
        import boto3
        assert boto3.__version__

    def test_botocore(self):
        import botocore
        assert botocore.__version__

    def test_s3fs(self):
        import s3fs
        assert s3fs.__version__


class TestEODHPackages:
    """Test EODH platform package imports."""

    def test_pyeodh(self):
        import pyeodh
        assert pyeodh.__version__

    def test_s3contents(self):
        import s3contents
        # s3contents may not have __version__

    def test_hybridcontents(self):
        import hybridcontents
        # hybridcontents may not have __version__


class TestKernels:
    """Test that Jupyter kernels are available."""

    def test_python_kernel(self):
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


class TestGDALDrivers:
    """Test that required GDAL drivers are available."""

    def test_required_drivers(self):
        from osgeo import gdal
        required_drivers = ["GTiff", "COG", "netCDF", "HDF5", "Zarr", "VRT"]
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
