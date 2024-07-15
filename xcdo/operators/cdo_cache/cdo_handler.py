import os
import re
import subprocess
from .interfaces import ICdoHandler
import typing as t
from .types import commandsType
from .exceptions import CdoError


class CdoHandler(ICdoHandler):
    def __init__(self, cdo: str = "cdo") -> None:
        self._cdo = cdo
        try:
            subprocess.run([cdo])
        except FileNotFoundError:
            raise CdoError("Command 'cdo' not found")

    def run(self, commands: commandsType) -> None:
        ret = subprocess.run(
            [self._cdo, *commands],
        ).returncode
        if ret != 0:
            raise CdoError(returncode=ret)

    def get_input_files(self, commands: commandsType) -> t.Tuple[str, ...]:
        input_files = self._get_input_files(commands)
        return tuple(sorted(set(input_files)))

    def _get_input_files(self, commands: commandsType) -> t.List[str]:
        input_files: t.List[str] = []
        for command in commands:
            if command.startswith("-"):
                input_files.extend(self._get_input_files(command.split(",")[1:]))
            elif "=" in command:
                input_files.extend(self._get_input_files(command.split("=")[1:]))
            elif os.path.isfile(command):
                input_files.append(command)
        return input_files

    def version(self) -> str:
        output, _ = self._captured_run(("-V",))
        pattern = r"Climate Data Operators version (\d+\.\d+\.\d+)"

        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise CdoError("Could not find cdo version")

    def _captured_run(self, commands: commandsType) -> t.Tuple[str, str]:
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
