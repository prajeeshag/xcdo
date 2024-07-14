import re
import subprocess
from .interfaces import ICdoHandler
import typing as t
from .exceptions import CdoError


class CdoHandler(ICdoHandler):
    def __init__(self, cdo: str = "cdo") -> None:
        self._cdo = cdo
        try:
            subprocess.run([cdo])
        except FileNotFoundError:
            raise CdoError("Command 'cdo' not found")

    def run(self, argv: t.Tuple[str, ...]) -> None:
        ret = subprocess.run(
            [self._cdo, *argv],
        ).returncode
        if ret != 0:
            raise CdoError(returncode=ret)

    def get_input_files(self, commands: t.Tuple[str, ...]) -> t.Tuple[str]:
        raise NotImplementedError

    def version(self) -> str:
        output, _ = self.captured_run(("-V",))
        pattern = r"Climate Data Operators version (\d+\.\d+\.\d+)"

        match = re.search(pattern, output)
        if match:
            return match.group(1)
        else:
            raise CdoError("Could not find cdo version")

    def captured_run(self, argv: t.Tuple[str, ...]) -> t.Tuple[str, str]:
        ret = subprocess.run(
            [self._cdo, *argv],
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


#
#    def run(self, cdo: str, argv: t.Tuple[str, ...]) -> None:
#        """
#        Run cdo with arguments
#        : param argv: List of command line arguments to cdo
#        : raises CdoError: If the execution fails
#        """
#
#    @abstractmethod
#    def get_output_files(self, argv: t.Tuple[str, ...]) -> t.List[str]:
#        """
#        : param argv: List of command line arguments to cdo
#        : returns: list of input files from the argument list
#        """
#        pass
#
#    @abstractmethod
#    def get_input_files(
#        self,
#        argv: t.Tuple[str, ...],
#        exclude_files: t.List[str] = [],
#    ) -> t.Tuple[str, ...]:
#        """
#        : param argv: List of command line arguments to cdo
#        : param exclude_files: List of files to be excluded
#        : returns: list of input files from the argument list
#        """
#        pass
#
#    @abstractmethod
#    def version() -> str:
#        """
#        : returns: cdo version string
#        : raises CdoError: If can't find the version string
#        """
#        pass
