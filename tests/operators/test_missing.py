#
import numpy as np
import pytest
import xarray as xr

from xcdo import DatasetIn, XcdoError
from xcdo.operators.missing_values import SetMissExpr, settomiss  # adjust import


@pytest.fixture
def sample_ds() -> DatasetIn:
    data = xr.DataArray(
        np.array(
            [
                [0.0, 1.0],
                [2.0, 3.0],
            ]
        ),
        dims=("x", "y"),
        name="var",
    )
    return DatasetIn(data.to_dataset())


def _var(ds):
    return list(ds.data_vars.values())[0]


def test_settomiss_eq(sample_ds):
    out = settomiss(sample_ds, 1.0, SetMissExpr.eq)
    var = _var(out)

    expected = np.array(
        [
            [0.0, np.nan],
            [2.0, 3.0],
        ]
    )
    np.testing.assert_allclose(var.values, expected, equal_nan=True)


def test_settomiss_gt(sample_ds):
    out = settomiss(sample_ds, 1.0, SetMissExpr.gt)
    var = _var(out)

    expected = np.array(
        [
            [0.0, 1.0],
            [np.nan, np.nan],
        ]
    )
    np.testing.assert_allclose(var.values, expected, equal_nan=True)


def test_settomiss_lt(sample_ds):
    out = settomiss(sample_ds, 1.0, SetMissExpr.lt)
    var = _var(out)

    expected = np.array(
        [
            [np.nan, 1.0],
            [2.0, 3.0],
        ]
    )
    np.testing.assert_allclose(var.values, expected, equal_nan=True)


def test_settomiss_ge(sample_ds):
    out = settomiss(sample_ds, 2.0, SetMissExpr.ge)
    var = _var(out)

    expected = np.array(
        [
            [0.0, 1.0],
            [np.nan, np.nan],
        ]
    )
    np.testing.assert_allclose(var.values, expected, equal_nan=True)


def test_settomiss_le(sample_ds):
    out = settomiss(sample_ds, 1.0, SetMissExpr.le)
    var = _var(out)

    expected = np.array(
        [
            [np.nan, np.nan],
            [2.0, 3.0],
        ]
    )
    np.testing.assert_allclose(var.values, expected, equal_nan=True)


def test_settomiss_unknown(sample_ds):
    with pytest.raises(XcdoError, match="Unknown expression"):
        settomiss(sample_ds, 1.0, "unknown")
