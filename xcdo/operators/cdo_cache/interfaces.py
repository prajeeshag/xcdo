from abc import ABC, abstractmethod
import typing as t
from .types import commandsType


class ICdoHandler(ABC):
    """
    Cdo Handler Abstract Class
    """

    @abstractmethod
    def run(self, commands: commandsType) -> None:
        """
        Run cdo with arguments

        Raises:
            CdoError: If the execution fails
        """

    @abstractmethod
    def get_input_files(
        self,
        commands: commandsType,
    ) -> t.Tuple[str, ...]:
        """
        Get the input files from cdo commands
        Returns:
            - tuple of input files if input files found
            - empty tuple if not input files found
        Raises:
            CdoError: If failed to find input files
        """

    @abstractmethod
    def version(self) -> str:
        """
        Returns: cdo version string

        Raises:
            CdoError: If can't find the version string
        """


class ICacheHandler(ABC):

    @abstractmethod
    def generate_cache_paths(self, noutputs: int, hash_code: str) -> t.Tuple[str, ...]:
        """
        Generates valid cache paths

        Ensures that the directory trees for the paths are created.

        Returns:
            - path strings: Tuple[str,...]
        """
        pass

    @abstractmethod
    def cache_exists(self, cache_files: t.Tuple[str, ...]) -> bool:
        """
        Returns:
            - True: if all cache_files exist
            - False:
        Raises:
            CacheError:
                - if cache_files is empty
        """

    @abstractmethod
    def is_cache_valid(
        self,
        cache_files: t.Tuple[str, ...],
        input_files: t.Tuple[str, ...],
    ) -> bool:
        """
        Returns:
            - True: if the oldest cache_file is newer than latest input_file
            - True: if input_files empty
            - False:
        Raises:
            CacheError:
                - if cache_files empty
        """

    @abstractmethod
    def generate_hash(self, commands: t.Tuple[str, ...]) -> str:
        """
        Generate hash from a list of string
        Returns:
            - hash string: str
        Raises CacheError:
            - if commands empty
        """
