from pathlib import Path
import pytest
import typing as t

from xcdo.operators.cdo_cache.exceptions import CdoError
from xcdo.operators.cdo_cache.interfaces import ICdoHandler
from xcdo.operators.cdo_cache.cdo_handler import CdoHandler

from ._utils import randomcmd, randomfile, randomword


@pytest.fixture
def cdo_handler():
    return CdoHandler()


def test_correct_instance(cdo_handler: ICdoHandler):
    assert isinstance(cdo_handler, ICdoHandler)


class Test_run:
    def test_invalid_commands(self, cdo_handler: ICdoHandler):
        commands = (randomcmd(), randomcmd())
        with pytest.raises(CdoError):
            cdo_handler.run(commands)

    def test_valid_commands(self, cdo_handler: ICdoHandler, tmp_path: t.Any):
        commands = ("--help",)
        cdo_handler.run(commands)

        temp_file = randomfile(tmp_path)
        commands = f"-const,0,r90x45 {temp_file}".split()
        cdo_handler.run(commands)


class Test_get_input_files:
    def test_empty_commands(self, cdo_handler: ICdoHandler):
        result = cdo_handler.get_input_files(())

        assert result == (), "result should be empty"

    def test_no_file_like(self, cdo_handler: ICdoHandler):
        command = [randomcmd(), randomcmd()]

        result = cdo_handler.get_input_files(command)

        assert result == (), "result should be empty"

    class Test_with_input_files:
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = tuple(
                        [
                            randomfile(tmp_path),
                        ]
                    )
                    self.command = [
                        f"{randomcmd()},{randomword(n=4)}",
                        randomcmd(),
                        str(self.input_files[0]),
                    ]

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
            [Path(f).write_text(" ") for f in env.input_files]
            result = cdo_handler.get_input_files(env.command)
            expected = tuple(sorted(env.input_files))
            assert result == expected, env.input_files

    class Test_file_as_parameter(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = tuple((randomfile(tmp_path),))
                    self.command = [
                        f"{randomcmd()},{randomword(n=4)}",
                        f"{randomcmd()},{self.input_files[0]}",
                    ]

            return Env()

    class Test_file_as_kwarg(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = (randomfile(tmp_path),)
                    fi = self.input_files
                    self.command = [
                        f"{randomcmd()},{randomword(n=4)}={fi[0]}",
                    ]

            return Env()

    class Test_file_as_parameter_and_input(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = tuple([randomfile(tmp_path) for _ in range(2)])
                    fi = self.input_files
                    self.command = [
                        f"{randomcmd()},{fi[0]}",
                        randomcmd(),
                        str(fi[1]),
                    ]

            return Env()

    class Test_multiple_files_as_input(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = (
                        randomfile(tmp_path),
                        randomfile(tmp_path),
                    )
                    self.command = [
                        randomcmd(),
                        str(self.input_files[0]),
                        randomcmd(),
                        str(self.input_files[1]),
                    ]

            return Env()

    class Test_multiple_files_as_parameter(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = (
                        randomfile(tmp_path),
                        randomfile(tmp_path),
                    )
                    fi = self.input_files
                    self.command = [
                        f"{randomcmd()},{fi[0]},{fi[1]}",
                        randomcmd(),
                    ]

            return Env()

    class Test_multiple_files_as_kwarg(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = (
                        randomfile(tmp_path),
                        randomfile(tmp_path),
                    )
                    fi = self.input_files
                    self.command = [
                        f"{randomcmd()},{randomword(n=4)}={fi[0]},{randomword(n=4)}={fi[1]}",
                        randomcmd(),
                    ]

            return Env()

    class Test_multiple_files_as_parm_and_input(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = tuple(randomfile(tmp_path) for _ in range(4))
                    fi = self.input_files
                    self.command = [
                        f"{randomcmd()},{fi[0]},{fi[1]}",
                        f"{fi[3]}",
                        f"{randomcmd()}",
                        f"{fi[2]}",
                    ]

            return Env()

    class Test_return_unique_files(Test_with_input_files):
        def arrange(self, tmp_path: t.Any) -> t.Any:
            class Env:
                def __init__(self) -> None:
                    self.input_files = tuple(randomfile(tmp_path) for _ in range(2))
                    fi = self.input_files
                    self.command = [
                        f"{randomcmd()},{fi[0]},{fi[1]}",
                        f"{fi[0]}",
                        f"{randomcmd()}",
                        f"{fi[1]}",
                    ]

            return Env()


def test_version(cdo_handler: ICdoHandler):
    result = cdo_handler.version()
    assert isinstance(result, str)
