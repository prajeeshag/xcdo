# type: ignore
import numpy as np
import pytest
import xarray as xr

from xcdo import DatasetIn
from xcdo.operators.mer_stat import (
    mermax,
    mermean,
    mermin,
    merstd,
    mersum,
)


@pytest.fixture
def sample_ds() -> DatasetIn:
    lat = np.array([-10, 0, 10], dtype=float)
    lon = np.array([0, 1], dtype=float)

    data = xr.DataArray(
        np.array(
            [
                [1.0, 2.0],  # latitude -10
                [3.0, 4.0],  # latitude 0
                [5.0, 6.0],  # latitude 10
            ]
        ),
        dims=("latitude", "longitude"),
        coords={"latitude": lat, "longitude": lon},
        name="var",
    )

    return DatasetIn(data.to_dataset())


def _get(sample_ds):
    return lambda ds: list(ds.data_vars.values())[0]


def test_mermean(sample_ds):
    out = mermean(sample_ds)
    var = _get(sample_ds)(out)

    # mean along longitude → row-wise mean
    expected = np.array(
        [
            (1 + 2) / 2,
            (3 + 4) / 2,
            (5 + 6) / 2,
        ]
    )

    np.testing.assert_allclose(var.values, expected)


def test_mermin(sample_ds):
    out = mermin(sample_ds)
    var = _get(sample_ds)(out)
    expected = np.array([1.0, 3.0, 5.0])
    np.testing.assert_allclose(var.values, expected)


def test_mermax(sample_ds):
    out = mermax(sample_ds)
    var = _get(sample_ds)(out)
    expected = np.array([2.0, 4.0, 6.0])
    np.testing.assert_allclose(var.values, expected)


def test_merstd(sample_ds):
    out = merstd(sample_ds)
    var = _get(sample_ds)(out)

    # std along longitude (two values per row)
    expected = np.array(
        [
            np.std([1, 2], ddof=0),
            np.std([3, 4], ddof=0),
            np.std([5, 6], ddof=0),
        ]
    )

    np.testing.assert_allclose(var.values, expected)


def test_mersum(sample_ds):
    out = mersum(sample_ds)
    var = _get(sample_ds)(out)
    expected = np.array([1 + 2, 3 + 4, 5 + 6])
    np.testing.assert_allclose(var.values, expected)
