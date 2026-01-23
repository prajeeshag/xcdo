#
import numpy as np
import pytest
import xarray as xr

from xcdo import DatasetIn
from xcdo.operators.time_stat import (
    timemax,
    timemean,
    timemin,
    timestd,
    timesum,
)


@pytest.fixture
def sample_ds() -> DatasetIn:
    time = np.array([0, 1, 2], dtype=float)
    lat = np.array([-10, 0], dtype=float)
    lon = np.array([0, 1], dtype=float)

    # shape: (time, lat, lon) = (3, 2, 2)
    data = xr.DataArray(
        np.array(
            [
                [[1, 2], [3, 4]],  # t0
                [[2, 3], [4, 5]],  # t1
                [[3, 4], [5, 6]],  # t2
            ]
        ),
        dims=("time", "latitude", "longitude"),
        coords={"time": time, "latitude": lat, "longitude": lon},
        name="var",
    )

    return DatasetIn(data.to_dataset())


def _get(sample_ds):
    return lambda ds: list(ds.data_vars.values())[0]


def test_timemean(sample_ds):
    out = timemean(sample_ds)
    var = _get(sample_ds)(out)

    expected = np.array(
        [
            [(1 + 2 + 3) / 3, (2 + 3 + 4) / 3],
            [(3 + 4 + 5) / 3, (4 + 5 + 6) / 3],
        ]
    )

    np.testing.assert_allclose(var.values, expected)


def test_timemin(sample_ds):
    out = timemin(sample_ds)
    var = _get(sample_ds)(out)

    expected = np.array(
        [
            [1, 2],
            [3, 4],
        ]
    )

    np.testing.assert_allclose(var.values, expected)


def test_timemax(sample_ds):
    out = timemax(sample_ds)
    var = _get(sample_ds)(out)

    expected = np.array(
        [
            [3, 4],
            [5, 6],
        ]
    )

    np.testing.assert_allclose(var.values, expected)


def test_timestd(sample_ds):
    out = timestd(sample_ds)
    var = _get(sample_ds)(out)

    expected = np.array(
        [
            [np.std([1, 2, 3], ddof=0), np.std([2, 3, 4], ddof=0)],
            [np.std([3, 4, 5], ddof=0), np.std([4, 5, 6], ddof=0)],
        ]
    )

    np.testing.assert_allclose(var.values, expected)


def test_timesum(sample_ds):
    out = timesum(sample_ds)
    var = _get(sample_ds)(out)

    expected = np.array(
        [
            [1 + 2 + 3, 2 + 3 + 4],
            [3 + 4 + 5, 4 + 5 + 6],
        ]
    )

    np.testing.assert_allclose(var.values, expected)
