#

import numpy as np
import pytest
import xarray as xr

from xcdo import XcdoError
from xcdo.operators.selecting import sellonlatbox


def simple_xrdset180():
    lon = range(-180, 180, 10)
    lat = range(-90, 100, 10)
    varx, vary = np.meshgrid(lon, lat)
    data = xr.Dataset(
        {"varx": (("lat", "lon"), varx), "vary": (("lat", "lon"), vary)},
        coords={
            "lat": ("lat", lat, {"units": "degrees_north"}),
            "lon": ("lon", lon, {"units": "degrees_east"}),
        },
    )
    return data


def two_grid_xrdset():
    lon1 = range(-180, 180, 10)
    lat1 = range(-90, 100, 10)
    varx1, vary1 = np.meshgrid(lon1, lat1)
    lon2 = range(0, 360, 10)
    lat2 = range(-90, 10, 10)
    varx2, vary2 = np.meshgrid(lon2, lat2)
    data = xr.Dataset(
        {"var1": (("lat1", "lon1"), varx1), "var2": (("lat2", "lon2"), varx2)},
        coords={
            "lat1": ("lat1", lat1, {"units": "degrees_north"}),
            "lon1": ("lon1", lon1, {"units": "degrees_east"}),
            "lat2": ("lat2", lat2, {"units": "degrees_north"}),
            "lon2": ("lon2", lon2, {"units": "degrees_east"}),
        },
    )
    return data


def simple_xrdset360():
    lon = range(0, 360, 10)
    lat = range(-90, 100, 10)
    varx, vary = np.meshgrid(lon, lat)
    data = xr.Dataset(
        {"varx": (("lat", "lon"), varx), "vary": (("lat", "lon"), vary)},
        coords={
            "lat": ("lat", lat, {"units": "degrees_north"}),
            "lon": ("lon", lon, {"units": "degrees_east"}),
        },
    )
    return data


def create_integer_grid(nx=8, ny=6):
    # 1. Create integer logical indices
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y)  # logical 2D grids
    lon_2d = X + Y
    lat_2d = Y * 2 + X
    data = np.arange(nx * ny).reshape(ny, nx)
    ds = xr.Dataset(
        data_vars={"var": (("ly", "lx"), data)},
        coords={
            "longitude": (("ly", "lx"), lon_2d, {"units": "degrees_east"}),
            "latitude": (("ly", "lx"), lat_2d, {"units": "degrees_north"}),
        },
    )
    return ds


class DummyDS:
    pass


def ds():
    return DummyDS()


def test_wlon_greater_than_elon():
    with pytest.raises(XcdoError, match="Western longitude should be smaller"):
        sellonlatbox(ds(), 10, -5, -10, 10)


def test_slat_greater_than_nlat():
    with pytest.raises(XcdoError, match="Southern latitude should be smaller"):
        sellonlatbox(ds(), -10, 10, 20, 10)


def test_wlon_less_than_minus_180():
    with pytest.raises(XcdoError, match="larger than -180"):
        sellonlatbox(ds(), -181, 10, -10, 10)


def test_elon_greater_than_360():
    with pytest.raises(XcdoError, match="smaller than 360"):
        sellonlatbox(ds(), 10, 361, -10, 10)


def test_slat_less_than_minus_90():
    with pytest.raises(XcdoError, match="larger than -90"):
        sellonlatbox(ds(), -10, 10, -91, 10)


def test_nlat_greater_than_90():
    with pytest.raises(XcdoError, match="smaller than 90"):
        sellonlatbox(ds(), -10, 10, -10, 91)


def test_mixed_longitude_formats():
    with pytest.raises(XcdoError, match="either"):
        sellonlatbox(ds(), -10, 200, -10, 10)


def test_sellonlatbox_simple():
    data = simple_xrdset180()
    result = sellonlatbox(data, -50, 50, -20, 20)
    assert result["varx"].shape == (5, 11)
    assert result["vary"].shape == (5, 11)
    assert (
        result["vary"].lon == np.array([-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50])
    ).all()
    assert (result["vary"].lat == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"][:, 0] == np.array([-20, -10, 0, 10, 20])).all()
    assert (
        result["varx"][0, :]
        == np.array([-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50])
    ).all()


def test_sellonlatbox_wraparound180():
    data = simple_xrdset180()
    result = sellonlatbox(data, 170, 210, -20, 20)
    assert result["varx"].shape == (5, 5)
    assert result["vary"].shape == (5, 5)
    assert (result["vary"].lon == np.array([170, 180, 190, 200, 210])).all()
    assert (result["vary"].lat == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"][:, 0] == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["varx"][0, :] == np.array([170, -180, -170, -160, -150])).all()


def test_sellonlatbox_180_lon180():
    data = simple_xrdset180()
    result = sellonlatbox(data, 190, 210, -20, 20)
    assert result["varx"].shape == (5, 3)
    assert result["vary"].shape == (5, 3)
    assert (result["vary"].lon == np.array([190, 200, 210])).all()
    assert (result["vary"].lat == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"][:, 0] == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["varx"][0, :] == np.array([-170, -160, -150])).all()


def test_sellonlatbox_2grid():
    data = two_grid_xrdset()
    with pytest.raises(
        XcdoError, match="Cannot handle selection for datasets with multiple grids"
    ):
        sellonlatbox(data, -50, 50, -20, 20)


def test_sellonlatbox_wraparound360():
    data = simple_xrdset360()
    result = sellonlatbox(data, -20, 20, -20, 20)
    assert result["varx"].shape == (5, 5)
    assert result["vary"].shape == (5, 5)
    assert (result["vary"].lon == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"].lat == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"][:, 0] == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["varx"][0, :] == np.array([340, 350, 0, 10, 20])).all()


def test_sellonlatbox_360_negativelon():
    data = simple_xrdset360()
    result = sellonlatbox(data, -20, -10, -20, 20)
    assert result["varx"].shape == (5, 2)
    assert result["vary"].shape == (5, 2)
    assert (result["vary"].lon == np.array([-20, -10])).all()
    assert (result["vary"].lat == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"][:, 0] == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["varx"][0, :] == np.array([340, 350])).all()


def test_sellonlatbox_360_positivelon():
    data = simple_xrdset360()
    result = sellonlatbox(data, 10, 20, -20, 20)
    assert result["varx"].shape == (5, 2)
    assert result["vary"].shape == (5, 2)
    assert (result["vary"].lon == np.array([10, 20])).all()
    assert (result["vary"].lat == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["vary"][:, 0] == np.array([-20, -10, 0, 10, 20])).all()
    assert (result["varx"][0, :] == np.array([10, 20])).all()


def test_sellonlatbox_curvilinear_simple():
    lon, lat = np.meshgrid(range(-180, 180, 10), range(-90, 100, 10))
    data = xr.Dataset(
        data_vars={"var": (("y", "x"), lon)},
        coords={
            "lon": (("y", "x"), lon, {"units": "degrees_east"}),
            "lat": (("y", "x"), lat, {"units": "degrees_north"}),
        },
    )
    result = sellonlatbox(data, -50, 50, -20, 20)
    assert result["var"].shape == (5, 11)
    # TODO add more robust tests


def test_sellonlatbox_curvilinear_rot():
    data = create_integer_grid()
    result = sellonlatbox(data, 2, 7, 1, 5)
    assert result["var"].shape == (3, 6)
    # TODO add more robust tests


def test_sellonlatbox_curvilinear_empty():
    data = create_integer_grid()
    with pytest.raises(XcdoError, match="Selection is empty"):
        sellonlatbox(data, 20, 25, 20, 25)


def test_sellonlatbox_empty():
    lon, lat = np.meshgrid(range(0, 90, 10), range(0, 90, 10))
    data = xr.Dataset(
        data_vars={"var": (("y", "x"), lon)},
        coords={
            "lon": (("y", "x"), lon, {"units": "degrees_east"}),
            "lat": (("y", "x"), lat, {"units": "degrees_north"}),
        },
    )
    with pytest.raises(XcdoError, match="Selection is empty"):
        sellonlatbox(data, 10, 20, -30, -20)


def test_sellonlatbox_different_names():
    data = xr.Dataset(
        {"var": (("latitude", "longitude"), np.random.rand(10, 10))},
        coords={
            "latitude": (
                "latitude",
                np.linspace(-90, 90, 10),
                {"units": "degrees_north"},
            ),
            "longitude": (
                "longitude",
                np.linspace(-180, 180, 10),
                {"units": "degrees_east"},
            ),
        },
    )
    result = sellonlatbox(data, -50, 50, -20, 20)
    assert result["var"].shape == (2, 2)


def test_sellonlatbox_no_longitude():
    data = xr.Dataset(
        {"var": (("latitude", "longitude"), np.random.rand(10, 10))},
        coords={
            "latitude": (
                "latitude",
                np.linspace(-90, 90, 10),
                {"units": "degrees_north"},
            ),
            "longitude": (
                "longitude",
                np.linspace(-180, 180, 10),
            ),
        },
    )
    with pytest.raises(XcdoError, match="Longitude not found in coordinates"):
        sellonlatbox(data, -50, 50, -20, 20)


def test_sellonlatbox_no_latitude():
    data = xr.Dataset(
        {"var": (("latitude", "longitude"), np.random.rand(10, 10))},
        coords={
            "latitude": (
                "latitude",
                np.linspace(-90, 90, 10),
            ),
            "longitude": (
                "longitude",
                np.linspace(-180, 180, 10),
                {"units": "degrees_east"},
            ),
        },
    )
    with pytest.raises(XcdoError, match="Latitude not found in coordinates"):
        sellonlatbox(data, -50, 50, -20, 20)
