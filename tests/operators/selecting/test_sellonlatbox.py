# type: ignore

import numpy as np
import xarray as xr

from xcdo.operators.selecting import sellonlatbox


def test_sellonlatbox_simple():
    data = xr.Dataset(
        {"var": (("lat", "lon"), np.random.rand(10, 10))},
        coords={"lat": np.linspace(-90, 90, 10), "lon": np.linspace(-180, 180, 10)},
    )
    result = sellonlatbox(data, -50, 50, -20, 20)
    assert result["var"].shape == (3, 3)


def test_sellonlatbox_curvilinear():
    lon, lat = np.meshgrid(np.linspace(-180, 180, 10), np.linspace(-90, 90, 10))
    data = xr.Dataset(
        {"var": (("y", "x"), np.random.rand(10, 10))},
        coords={"lat": (("y", "x"), lat), "lon": (("y", "x"), lon)},
    )
    result = sellonlatbox(data, -50, 50, -20, 20)
    assert result["var"].shape == (3, 3)


def test_sellonlatbox_different_names():
    data = xr.Dataset(
        {"var": (("latitude", "longitude"), np.random.rand(10, 10))},
        coords={
            "latitude": np.linspace(-90, 90, 10),
            "longitude": np.linspace(-180, 180, 10),
        },
    )
    result = sellonlatbox(data, -50, 50, -20, 20)
    assert result["var"].shape == (3, 3)
