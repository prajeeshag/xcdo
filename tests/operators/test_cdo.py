# type: ignore
from unittest.mock import MagicMock, patch

import pytest
from xarray import Dataset

from xcdo import XcdoError
from xcdo.operators.cdo import cdo_run  # adjust import


def test_cdo_run_success(tmp_path):
    fake_out = tmp_path / "out.nc"

    with (
        patch("xcdo.operators.cdo.shutil.which", return_value="cdo"),
        patch("xcdo.operators.cdo.subprocess.check_call") as mock_call,
        patch("xcdo.operators.cdo.open_dataset", return_value=Dataset()) as mock_open,
        patch("tempfile.NamedTemporaryFile") as mock_tmp,
    ):
        # Fake temp file object
        tmp_file = MagicMock()
        tmp_file.__enter__.return_value.name = str(fake_out)
        mock_tmp.return_value = tmp_file

        ds = cdo_run("-timmean", "input.nc")

        mock_call.assert_called_once()
        args = mock_call.call_args[0][0]
        assert args[:4] == ["cdo", "-f", "nc", "-timmean"]
        assert args[-1] == str(fake_out)

        mock_open.assert_called_once_with(str(fake_out))
        assert isinstance(ds, Dataset)


def test_cdo_run_missing_cdo():
    with patch("xcdo.operators.cdo.shutil.which", return_value=None):
        with pytest.raises(XcdoError):
            cdo_run("-timmean", "input.nc")
