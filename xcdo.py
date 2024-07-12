import hashlib
import typing as t
import subprocess
import re
import sys
from pathlib import Path
from abc import ABC, abstractmethod


def _is_symlink_to(file_path: str, target_path: str) -> bool:
    file_path = Path(file_path)
    return file_path.is_symlink() and file_path.readlink() == Path(target_path)


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


def _files_exist(paths: t.List[str]) -> bool:
    for f in paths:
        if not Path(f).is_file():
            return False
    return True


def _generate_hash(strings: t.List[str]) -> str:
    combined_string = " ".join(strings)
    hash_object = hashlib.sha256(combined_string.encode())
    hash_code = hash_object.hexdigest()
    return hash_code


def _mv_and_link_back(file1: str, file2: str):
    pass


class XCdo:
    """
    A simple cdo wrapper class to enable cacheing.
    """

    _cachedir_name: str = ".cdocache"

    def __init__(self, cdo: ICdoHandler) -> None:
        self._cdo: ICdoHandler = cdo

    def __call__(self, argv: t.List[str]) -> int:
        """
        1. Should produce the same terminal outputs as calling a bare cdo
        2. Should return the same return code of cdo
        """
        if not argv:
            self._cdo.run(argv)
            return

        output_files = self._cdo.get_output_files(argv)
        if not output_files:
            self._cdo.run(argv)
            return

        cdo_version = self._cdo.version()
        first_output_index = argv.index(output_files[0])
        hash_code = _generate_hash([*argv[:first_output_index], cdo_version])
        cache_files = self._generate_cache_file_paths(hash_code, output_files)
        if all([_is_symlink_to(f, c) for f, c in cache_files.items()]):
            return
        self._cdo.run(argv)
        for f, c in cache_files.items():
            _mv_and_link_back(f, c)

        # self._futil.files_exist(output_files)
        # self._cdo.get_input_files(argv, exclude_files=output_files)
        # try:
        #    output_files = self._cdo.get_output_files(argv)
        #    processed_call = self._cdo.get_processed_call(argv)
        #    first_operator = processed_call[2]
        #    input_files = self._get_input_files((first_operator,))

        #    if first_operator in argv:
        #        first_operator_index = argv.index(first_operator)
        #    else:
        #        first_operator_index = argv.index("-" + first_operator)

        #    argv_without_output = argv[:first_output_index]

        #    input_files.update(
        #        self._get_input_files(argv_without_output[first_operator_index + 1 :])
        #    )
        #    hash_code = self._generate_hash([*argv_without_output, cdo_version])

        #    all_cache_files_exists = all(
        #        [Path(c).is_file() for f, c in cache_files.items()]
        #    )

        #    is_all_cache_linked = all(
        #        [_is_symlink_to(f, c) for f, c in cache_files.items()]
        #    )

        #    if is_all_cache_linked:
        #        return 0

        #    if all_cache_files_exists:
        #        try:
        #            for f, c in cache_files.items():
        #                Path(f).symlink_to(c)
        #            return 0
        #        except OSError:
        #            raise (CdoError(f"Could not symlink {f} -> {c}"))

        #    output_files_exists = all([Path(f) for f in output_files])

        # except CdoError as e:
        #    print(f"Warning: {str(e)}")
        #    return self._cdo.run(argv)

    def _generate_cache_file_paths(
        self,
        hash_code: str,
        output_files: t.List[str],
    ) -> t.Dict[str, str]:
        res: t.Dict[str, str] = {}

        for i, f in enumerate(output_files):
            ipath = Path(f)
            cpath = ipath.parent / self._cachedir_name / hash_code
            res[f] = str(cpath)

        return res

    def _get_input_files(self, argv: t.List[str]) -> t.Set[str]:
        """
        It expects all operators in the argv to be dashed.

        All comma separated parameters of operators will be returned as input files if it exist as a file
        However, this can lead to unneccesarily recalculations for e.g.
        xcdo -subc,10 in.nc out.nc
        touch 10
        xcdo -subc,10 in.nc out.nc
        """
        res: t.Set[str] = set()
        apply_syntax = ("[", "]", ":")
        for arg in argv:
            if not arg:  # For some reason if it is empty string
                continue
            if arg in apply_syntax:  # The --apply & --argument_groups
                continue
            if arg.startswith("-"):
                arg_words = arg.split(",")
                if len(arg_words) > 1:
                    res.update(self._get_input_files(arg_words[1:]))
            elif "=" in arg:
                arg_words = arg.split("=")
                res.update(self._get_input_files(arg_words))
            elif Path(arg).is_file():
                res.add(arg)
        return res

    def _get_output_files(self, argv: t.List[str]) -> t.List[str]:
        processed_call = self._cdo.get_processed_call(argv)
        o1 = processed_call.split()[0]
        try:
            o1_index = argv.index(o1)
        except ValueError:
            return ()

        if o1_index == len(argv) - 1:
            return (o1,)

        o2_index = o1_index + 1

        if argv[o2_index].lstrip("-") in processed_call:
            return ()

        return tuple(argv[o1_index:])


def main():
    print(sys.argv[0])
    cdo = Cdo()
    sys.exit(cdo(sys.argv[1:]))


if __name__ == "__main__":
    main()
