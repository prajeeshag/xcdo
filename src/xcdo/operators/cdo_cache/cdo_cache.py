from dataclasses import dataclass

from .interfaces import ICacheHandler, ICdoHandler
from .types import argvType


@dataclass
class CdoCache:
    _cdo: ICdoHandler
    _cache: ICacheHandler

    def get_cache(self, argv: argvType, n_outputs: int) -> tuple[str, ...]:
        if not argv:
            raise ValueError("no commands provided")
        if n_outputs < 1:
            raise ValueError("n_outputs should be a positive integer")
        cdo_version = self._cdo.version()
        input_files = self._cdo.get_input_files(argv)
        hash_code = self._cache.generate_hash((*argv, cdo_version, *input_files))
        cache_files = self._cache.generate_cache_paths(n_outputs, hash_code)
        if not self._cache.cache_exists(cache_files):
            self._cdo.run((*argv, *cache_files))
            return cache_files
        if input_files and not self._cache.is_cache_valid(cache_files, input_files):
            self._cdo.run((*argv, *cache_files))
        return cache_files
