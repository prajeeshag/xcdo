# type: ignore
import xarray as xr

from xcdo.operators.misc import merge


def test_merge_calls_xr_merge(mocker):
    mock_merge = mocker.patch("xcdo.operators.misc.xr.merge", return_value="merged")

    ds1 = xr.Dataset({"a": ("x", [1])})
    ds2 = xr.Dataset({"b": ("x", [2])})

    result = merge(
        ds1, ds2, compat="no_conflicts", join="outer", combine_attrs="override"
    )

    mock_merge.assert_called_once_with(
        (ds1, ds2),
        compat="no_conflicts",
        join="outer",
        combine_attrs="override",
    )
    assert result == "merged"
