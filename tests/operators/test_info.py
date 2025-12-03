# type: ignore
from unittest.mock import patch

import numpy as np
import pytest
import xarray as xr

from xcdo import DatasetIn
from xcdo.operators.info import showtimestamp  # adjust import


@pytest.fixture
def sample_ds() -> DatasetIn:
    data = xr.DataArray(
        np.array([1.0, 2.0, 3.0]),
        dims=("time",),
        coords={
            "time": np.array(
                ["2000-01-01", "2000-01-02", "2000-01-03"],
                dtype="datetime64[ns]",
            )
        },
        name="var",
    )
    return DatasetIn(data.to_dataset())


def test_showtimestamp_prints(sample_ds):
    with patch("builtins.print") as mock_print:
        showtimestamp(sample_ds)

    # ensure print was called exactly once
    mock_print.assert_called_once()

    # extract the first positional argument passed to print
    printed_arg = mock_print.call_args[0][0]

    expected = sample_ds.cf["time"].values
    np.testing.assert_array_equal(printed_arg, expected)


def test_showtimestamp_no_time():
    data = xr.DataArray(
        np.array([1, 2]),
        dims=("x",),
        coords={"x": [10, 20]},
        name="var",
    )
    ds = DatasetIn(data.to_dataset())

    with pytest.raises(ValueError, match="No 'time' coordinate"):
        showtimestamp(ds)
