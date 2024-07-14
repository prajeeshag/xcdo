import pytest
import typing as t

from xcdo.operators.cdo_cache.exceptions import CdoError
from xcdo.operators.cdo_cache.interfaces import ICdoHandler
from xcdo.operators.cdo_cache.cdo_handler import CdoHandler


@pytest.fixture
def cdo_handler():
    return CdoHandler()


def test_correct_instance(cdo_handler: ICdoHandler):
    assert isinstance(cdo_handler, ICdoHandler)


class TestRun:
    def test_invalid_commands(self, cdo_handler: ICdoHandler):
        commands = ("-some", "-command")
        with pytest.raises(CdoError):
            cdo_handler.run(commands)

    def test_valid_commands(self, cdo_handler: ICdoHandler):
        commands = ("--help",)
        cdo_handler.run(commands)


def test_version(cdo_handler: ICdoHandler):
    result = cdo_handler.version()
    assert isinstance(result, str)
