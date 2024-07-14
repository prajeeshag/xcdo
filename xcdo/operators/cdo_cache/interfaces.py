from abc import ABC, abstractmethod
import typing as t


class ICdoHandler(ABC):
    """
    Cdo Handler Abstract Class
    """

    @abstractmethod
    def run(self, argv: t.Tuple[str, ...]) -> None:
        """
        Run cdo with arguments

        Raises:
            CdoError: If the execution fails
        """

    @abstractmethod
    def get_input_files(
        self,
        commands: t.Tuple[str, ...],
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
    def version() -> str:
        """
        Returns: cdo version string

        Raises:
            CdoError: If can't find the version string
        """


class ICacheHandler(ABC):

    @abstractmethod
    def ensure_directories_exist(self, paths: t.Tuple[str, ...]) -> None:
        """
        Ensures that the directory trees for the given paths are created.

        Args:
            paths (Tuple[str, ...]): A tuple of paths for which to create directory trees.

        Raises CacheError:
            - If any error occurs during directory creation, re-raises it with additional context.
        """
        pass

    @abstractmethod
    def generate_cache_paths(self, noutputs: int, hash_code: str) -> t.Tuple[str, ...]:
        """
        Generates valid cache paths

        Ensures that if the generated path contains directories, the directory tree is created.

        Returns:
            - path strings: Tuple[str,...]

        Raises CacheError:
            - if noutputs is not a positive integer
            - if any other Exception occurs, re-raise it with additional context
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
                - if any other Exception occurs, re-raise it with additional context
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
                - if any other Exception occurs, re-raise it with additional context
        """

    @abstractmethod
    def generate_hash(self, commands: t.Tuple[str, ...]) -> str:
        """
        Generate hash from a list of string
        Returns:
            - hash string: str
        Raises CacheError:
            - if commands empty
            - if any other Exception occurs, re-raise it with additional context
        """
