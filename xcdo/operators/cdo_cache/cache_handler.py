# import hashlib
import hashlib
import os

from .exceptions import CacheError
from .interfaces import ICacheHandler
from .types import argvType


class CacheHandler(ICacheHandler):
    _file_prefix = ".cdo_cache_"

    def ensure_directories_exist(self, paths: argvType) -> None:
        raise NotImplementedError

    def generate_cache_paths(self, noutputs: int, hash_code: str) -> tuple[str, ...]:
        cache_paths: list[str] = []
        for i in range(noutputs):
            cache_paths.append(f"{self._file_prefix}{i}_{hash_code}")
        return tuple(cache_paths)

    def cache_exists(self, cache_files: argvType) -> bool:
        if not cache_files:
            raise CacheError("no cache files provided")
        for f in cache_files:
            if not os.path.isfile(f):
                return False
        return True

    def is_cache_valid(self, cache_files: argvType, input_files: argvType) -> bool:
        if not cache_files:
            return False

        for c in cache_files:
            if not os.path.isfile(c):
                return False

        if not input_files:
            return True

        latest_input_file = max(input_files, key=os.path.getmtime)
        oldest_cache_file = min(cache_files, key=os.path.getmtime)

        return os.path.getmtime(latest_input_file) < os.path.getmtime(oldest_cache_file)

    def generate_hash(self, argv: argvType) -> str:
        if not argv:
            raise CacheError("empty commands")

        combined_string = " ".join(argv)
        hash_object = hashlib.sha256(combined_string.encode())
        hash_code = hash_object.hexdigest()
        return hash_code
