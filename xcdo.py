import hashlib
import typing as t
import subprocess
import re
import sys
from pathlib import Path
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
    def __init__(self, cdo="cdo") -> None:
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
    def get_output_files(argv: t.List[str]) -> t.List[str]:
        """
        : param argv: List of command line arguments to cdo
        : returns: list of input files from the argument list
        """
        pass

    @abstractmethod
    def get_input_files(
        argv: t.List[str],
        exclude_files: t.List[str] = [],
    ) -> t.List[str]:
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
    def run(self, argv: t.List[str]) -> None:
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
        : returns: The capture output as string
        : raises CdoError: If the execution fails
        """


class _Utils:
    def _is_symlink_to(self, file_path: str, target_path: str) -> bool:
        file_path = Path(file_path)
        return file_path.is_symlink() and file_path.readlink() == Path(target_path)

    def are_all_linked_to(
        self,
        file_paths: t.List[str],
        target_paths: t.List[str],
    ) -> bool:
        pass

    def link_all(self, file_path: t.List[str], target_path: t.List[str]) -> None:
        pass

    def generate_hash(self, strings: t.List[str]) -> str:
        combined_string = " ".join(strings)
        hash_object = hashlib.sha256(combined_string.encode())
        hash_code = hash_object.hexdigest()
        return hash_code

    def move_all(self, files1: t.List[str], files2: t.List[str]) -> None:
        pass

    def all_files_exist(self, files: t.List[str]) -> bool:
        pass

    def is_any_file_new(self, files1: t.List[str], files2: t.List[str]) -> bool:
        pass


class XCdo:
    """
    A simple cdo wrapper class to enable cacheing.
    """

    _cachedir_name: str = ".cdocache"

    def __init__(self, cdo: ICdoHandler) -> None:
        self._cdo: ICdoHandler = cdo

    def __call__(self, argv: t.List[str]) -> int:
        return self._run(argv=argv)

    def _run(self, argv: t.List[str]) -> int:
        """
        1. Should produce the same terminal outputs as calling a bare cdo
        2. Should return the same return code of cdo
        """
        if not argv:
            self._cdo.run(argv)
            return

        utils = _Utils()

        output_files = self._cdo.get_output_files(argv)
        if not output_files:
            self._cdo.run(argv)
            return

        cdo_version = self._cdo.version()
        first_output_index = argv.index(output_files[0])
        hash_code = utils.generate_hash([*argv[:first_output_index], cdo_version])
        cache_files = self._generate_cache_file_paths(hash_code, output_files)

        if not utils.all_files_exist(cache_files):
            return self._run_and_cache(argv, output_files, cache_files)

        input_files = self._cdo.get_input_files(argv, exclude_files=output_files)

        if not utils.is_any_file_new(input_files, cache_files):
            return self._run_and_cache(argv, output_files, cache_files)

        if not utils.are_all_linked_to(output_files, cache_files):
            utils.link_all(output_files, cache_files)

    def _run_and_cache(
        self,
        argv,
        output_files,
        cache_files,
    ) -> None:
        utils = _Utils()
        self._cdo.run(argv)
        utils.move_all(output_files, cache_files)
        utils.link_all(output_files, cache_files)

    def _generate_cache_file_paths(
        self,
        hash_code: str,
        output_files: t.List[str],
    ) -> t.List[str]:
        res: t.List[str] = []

        for i, f in enumerate(output_files):
            ipath = Path(f)
            cpath = ipath.parent / self._cachedir_name / f"{hash_code}_{i}"
            res.append(str(cpath))

        return res


def main():
    print(sys.argv[0])
    cdo = Cdo()
    sys.exit(cdo(sys.argv[1:]))


if __name__ == "__main__":
    main()
