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

    def test_valid_commands(self, cdo_handler: ICdoHandler, tmp_path: t.Any):
        commands = ("--help",)
        cdo_handler.run(commands)

        temp_file = tmp_path / "out.nc"
        commands = f"-const,0,r90x45 {temp_file}".split()
        cdo_handler.run(commands)


class TestInputFiles:
    def test_empty_commands(self, cdo_handler: ICdoHandler):
        result = cdo_handler.get_input_files(())

        assert result == (), "result should be empty"

    class TestValidCommand:
        def test_no_file_like(self, cdo_handler: ICdoHandler):
            command = tuple("-somecommand -anothercommand".split())

            result = cdo_handler.get_input_files(command)

            assert result == (), "result should be empty"

        class TestFileAsInput:
            def arrange(self, tmp_path: t.Any) -> t.Any:
                class Env:
                    def __init__(self) -> None:
                        self.input_file = tmp_path / "input.nc"
                        self.command = (
                            f"-somecommand,1 -anothercommand {self.input_file}".split()
                        )

                return Env()

            def test_file_does_not_exist(
                self,
                cdo_handler: ICdoHandler,
                tmp_path: t.Any,
            ):
                env = self.arrange(tmp_path=tmp_path)
                result = cdo_handler.get_input_files(env.command)
                assert result == (), "result should be empty"

            def test_file_exist(self, cdo_handler: ICdoHandler, tmp_path: t.Any):
                env = self.arrange(tmp_path=tmp_path)
                env.input_file.write_text("")
                result = cdo_handler.get_input_files(env.command)
                assert result == (str(env.input_file),)

        class TestFileAsParameter(TestFileAsInput):
            def arrange(self, tmp_path: t.Any) -> t.Any:
                class Env:
                    def __init__(self) -> None:
                        self.input_file = tmp_path / "input.nc"
                        self.command = (
                            f"-somecommand,1 -anothercommand,{self.input_file}".split()
                        )

                return Env()


def test_version(cdo_handler: ICdoHandler):
    result = cdo_handler.version()
    assert isinstance(result, str)
