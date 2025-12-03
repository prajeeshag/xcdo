# tests/test_selection_ops.py
from unittest.mock import MagicMock

import pytest

from xcdo import XcdoError
from xcdo.operators.selecting import isel, selvar


def test_selvar_success():
    # mock dataset
    mock_ds = MagicMock()
    mock_var_ds = MagicMock()
    mock_ds.data_vars = {"tas": MagicMock(to_dataset=lambda: mock_var_ds)}

    mock_input = MagicMock()
    mock_input.data_vars = mock_ds.data_vars

    out = selvar(mock_input, "tas")
    assert out is mock_var_ds


def test_selvar_missing_variable():
    mock_input = MagicMock()
    mock_input.data_vars = {"pr": MagicMock()}

    with pytest.raises(XcdoError) as e:
        selvar(mock_input, "tas")

    assert "`tas` is not a data variable" in str(e.value)


def test_isel_forwarding_indexes():
    mock_ds = MagicMock()
    mock_result = MagicMock()
    mock_ds.isel.return_value = mock_result

    mock_input = mock_ds
    out = isel(mock_input, time=0, lon=5)

    mock_input.isel.assert_called_once_with({"time": 0, "lon": 5})
    assert out is mock_result
