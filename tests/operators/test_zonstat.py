# type: ignore
import numpy as np
import pytest
import xarray as xr

from xcdo import DatasetIn
from xcdo.operators.zon_stat import (
    zonmax,
    zonmean,
    zonmin,
    zonstd,
    zonsum,
)


@pytest.fixture
def sample_ds() -> DatasetIn:
    lat = np.array([-10, 0, 10], dtype=float)
    lon = np.array([0, 1], dtype=float)

    data = xr.DataArray(
        np.array(
            [
                [1.0, 2.0],  # lat -10
                [3.0, 4.0],  # lat 0
                [5.0, 6.0],  # lat 10
            ]
        ),
        dims=("latitude", "longitude"),
        coords={"latitude": lat, "longitude": lon},
        name="var",
    )

    return DatasetIn(data.to_dataset())


def _get(sample_ds):
    # utility to extract the variable from returned DatasetOut
    return lambda ds: list(ds.data_vars.values())[0]


def test_zonmean(sample_ds):
    out = zonmean(sample_ds)
    var = _get(sample_ds)(out)
    # mean over latitude
    expected = np.array([(1 + 3 + 5) / 3, (2 + 4 + 6) / 3])
    np.testing.assert_allclose(var.values, expected)


def test_zonmin(sample_ds):
    out = zonmin(sample_ds)
    var = _get(sample_ds)(out)
    expected = np.array([1.0, 2.0])
    np.testing.assert_allclose(var.values, expected)


def test_zonmax(sample_ds):
    out = zonmax(sample_ds)
    var = _get(sample_ds)(out)
    expected = np.array([5.0, 6.0])
    np.testing.assert_allclose(var.values, expected)


def test_zonstd(sample_ds):
    out = zonstd(sample_ds)
    var = _get(sample_ds)(out)

    # std for each longitude
    col0 = np.std([1, 3, 5], ddof=0)
    col1 = np.std([2, 4, 6], ddof=0)
    expected = np.array([col0, col1])

    np.testing.assert_allclose(var.values, expected)


def test_zonsum(sample_ds):
    out = zonsum(sample_ds)
    var = _get(sample_ds)(out)
    expected = np.array([1 + 3 + 5, 2 + 4 + 6])
    np.testing.assert_allclose(var.values, expected)
