# from dataclasses import dataclass
# import subprocess
# from .interfaces import ICdoHandler
# import typing as t
# from .exceptions import CdoError


# @dataclass
# class CdoHandler(ICdoHandler):
#     _cdo: str

#     def captured_run(self, argv: t.List[str]) -> t.Tuple[str, str]:
#         ret = subprocess.run(
#             [self._cdo, *argv],
#             capture_output=True,
#         )
#         if ret.returncode != 0:
#             raise CdoError(
#                 stdout=ret.stdout.decode(),
#                 stderr=ret.stderr.decode(),
#                 returncode=ret.returncode,
#             )
#         return (
#             ret.stdout.decode(),
#             ret.stderr.decode(),
#         )


#
#    def run(self, cdo: str, argv: t.Tuple[str, ...]) -> None:
#        """
#        Run cdo with arguments
#        : param argv: List of command line arguments to cdo
#        : raises CdoError: If the execution fails
#        """
#        ret = subprocess.run(
#            [cdo, *argv],
#        ).returncode
#        if ret != 0:
#            raise CdoError(returncode=ret)
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
