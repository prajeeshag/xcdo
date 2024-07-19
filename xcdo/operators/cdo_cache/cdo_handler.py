import os
import re
import subprocess

from .exceptions import CdoError
from .interfaces import ICdoHandler
from .types import argvType


class CdoHandler(ICdoHandler):
    def __init__(self, cdo: str = "cdo") -> None:
        self._cdo = cdo
        try:
            subprocess.run([cdo])
        except FileNotFoundError:
            raise CdoError("Command 'cdo' not found")

    def run(self, argv: argvType) -> None:
        ret = subprocess.run(
            [self._cdo, *argv],
        ).returncode
        if ret != 0:
            raise CdoError(returncode=ret)

    def get_input_files(self, argv: argvType) -> tuple[str, ...]:
        input_files = self._get_input_files(argv)
        return tuple(sorted(set(input_files)))

    def _get_input_files(self, argv: argvType) -> list[str]:
        input_files: list[str] = []
        for arg in argv:
            if arg.startswith("-"):
                input_files.extend(self._get_input_files(arg.split(",")[1:]))
            elif "=" in arg:
                input_files.extend(self._get_input_files(arg.split("=")[1:]))
            elif os.path.isfile(arg):
                input_files.append(arg)
        return input_files

    def version(self) -> str:
        output, _ = self._captured_run(("-V",))
        pattern = r"Climate Data Operators version (\d+\.\d+\.\d+)"

        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise CdoError("Could not find cdo version")

    def _captured_run(self, commands: argvType) -> tuple[str, str]:
        ret = subprocess.run(
            [self._cdo, *commands],
            capture_output=True,
        )
        if ret.returncode != 0:
            raise CdoError(
                stdout=ret.stdout.decode(),
                stderr=ret.stderr.decode(),
                returncode=ret.returncode,
            )
        return (
            ret.stdout.decode(),
            ret.stderr.decode(),
        )
