# type: ignore
import sys
from unittest.mock import MagicMock, patch

import pytest

from xcdo.exceptions import XcdoError
from xcdo.operators.plotting import plot  # adjust import


def test_plot_missing_matplotlib(monkeypatch):
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", None)  # force ImportError

    class DummyIn:
        pass

    with pytest.raises(XcdoError, match="`matplotlib` is not installed"):
        plot(DummyIn())  # should fail at import


def test_plot_calls(monkeypatch):
    # mock darray and its plot()
    mock_darray = MagicMock()
    mock_darray.plot = MagicMock()

    # mock DatasetIn
    mock_input = MagicMock()
    mock_input.get_dataarray.return_value = mock_darray

    # mock plt.show
    with patch("matplotlib.pyplot.show") as mock_show:
        plot(mock_input)

    mock_input.get_dataarray.assert_called_once()
    mock_darray.plot.assert_called_once()
    mock_show.assert_called_once()


def test_plot_savefig(monkeypatch):
    # mock darray and its plot()
    mock_darray = MagicMock()
    mock_darray.plot = MagicMock()

    # mock DatasetIn
    mock_input = MagicMock()
    mock_input.get_dataarray.return_value = mock_darray

    # mock plt.show
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        plot(mock_input, "test.png")

    mock_input.get_dataarray.assert_called_once()
    mock_darray.plot.assert_called_once()
    mock_savefig.assert_called_once_with("test.png")
