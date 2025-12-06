# type: ignore
import xarray as xr

from xcdo.operators.misc import print_dataset


def test_print_dataset_calls_rich_print(mocker):
    mock_print = mocker.patch("xcdo.operators.misc.rich.print")

    ds = xr.Dataset({"a": ("x", [1, 2, 3])})
    print_dataset(ds)

    mock_print.assert_called_once_with(ds)
