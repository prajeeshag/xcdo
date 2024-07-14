import hashlib
import typing as t
import subprocess
import re
from abc import ABC, abstractmethod


class CdoWarning(Warning):
    pass


class CdoError(Exception):
    def __init__(
        self, msg: str = "", stdout: str = "", stderr: str = "", returncode: int = 1
    ):
        super().__init__(msg)
        self.msg: str = msg
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.returncode: int = returncode

    def __str__(self) -> str:
        res = ""
        res += f"{self.stdout}\n\n" if self.stdout else ""
        res += f"{self.stderr}\n\n" if self.stderr else ""
        res += f"---\n{self.msg}" if self.msg else ""
        return res


class Cdo:
    def __init__(self, cdo: str = "cdo") -> None:
        self.CDO = cdo
        pass

    def captured_run(self, argv: t.List[str]):
        ret = subprocess.run(
            [self.CDO, *argv],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if ret.returncode != 0:
            raise CdoError(
                stdout=ret.stdout.decode(),
                stderr=ret.stderr.decode(),
                returncode=ret.returncode,
            )
        return ret.stdout.decode("utf-8")

    ## TODO: this shouldn't be here
    def get_processed_call(self, argv: t.List[str]) -> str:
        return self.captured_run(["-A", *argv])

    ## TODO: this shouldn't be here
    def version(self) -> str:
        cdo_help = self.captured_run(["-V"])
        match = re.search(r"Climate Data Operators version (\d.*) .*", cdo_help)
        if match is None:
            raise CdoError(msg="Could not find version string")
        return match.group(1)

    def run(self, input: t.List[str]):
        ret = subprocess.run(
            [self.CDO, *input],
        ).returncode
        if ret != 0:
            raise CdoError(returncode=ret)


class ICdoHandler(ABC):
    """
    Cdo Handler Interface
    """

    @abstractmethod
    def get_output_files(self, argv: t.Tuple[str, ...]) -> t.List[str]:
        """
        : param argv: List of command line arguments to cdo
        : returns: list of input files from the argument list
        """
        pass

    @abstractmethod
    def get_input_files(
        self,
        argv: t.Tuple[str, ...],
        exclude_files: t.List[str] = [],
    ) -> t.Tuple[str, ...]:
        """
        : param argv: List of command line arguments to cdo
        : param exclude_files: List of files to be excluded
        : returns: list of input files from the argument list
        """
        pass

    @abstractmethod
    def version() -> str:
        """
        : returns: cdo version string
        : raises CdoError: If can't find the version string
        """
        pass

    @abstractmethod
    def run(self, argv: t.Tuple[str, ...]) -> None:
        """
        Run cdo with arguments
        : param argv: List of command line arguments to cdo
        : raises CdoError: If the execution fails
        """

    @abstractmethod
    def captured_run(self, argv: t.List[str]):
        """
        Run cdo with arguments
        : param argv: List of command line arguments to cdo
        : returns: The captured output as string
        : raises CdoError: If the execution fails
        """


class Utils(ABC):

    @abstractmethod
    def generate_cache_paths(self, noutputs: int, hash_code: str) -> t.Tuple[str, ...]:
        pass

    @abstractmethod
    def cache_exists(self, paths: t.Tuple[str, ...]) -> bool:
        pass

    @abstractmethod
    def is_cache_valid(
        self,
        cache_files: t.Tuple[str, ...],
        input_files: t.Tuple[str, ...],
    ) -> bool:
        pass

    def generate_hash(self, strings: t.Tuple[str, ...]) -> str:
        """
        Generate hash from a list of string
        """
        combined_string = " ".join(strings)
        hash_object = hashlib.sha256(combined_string.encode())
        hash_code = hash_object.hexdigest()
        return hash_code


class CdoCache:
    """
    A simple cdo wrapper class to enable cacheing.
    """

    _cachedir_name: str = ".cdocache"

    def __init__(self, cdo: ICdoHandler, utils: Utils) -> None:
        self._cdo: ICdoHandler = cdo
        self._utils: Utils = utils

    def execute(
        self, commands: t.Tuple[str, ...], noutputs: int = 1
    ) -> t.Tuple[str, ...]:
        if not commands:
            raise ValueError("no commands provided")
        if noutputs < 1:
            raise ValueError("noutputs should be a positive integer")

        hash_code = self._utils.generate_hash(commands)

        cache_files = self._utils.generate_cache_paths(noutputs, hash_code)

        if not self._utils.cache_exists(cache_files):
            self._cdo.run((*commands, *cache_files))
            return cache_files

        input_files = self._cdo.get_input_files(commands)
        if input_files and not self._utils.is_cache_valid(cache_files, input_files):
            self._cdo.run((*commands, *cache_files))
        return cache_files
