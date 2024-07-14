import typing as t
from .interfaces import ICacheHandler, ICdoHandler


class CdoCache:
    """
    A simple cdo wrapper class to enable cacheing.
    """

    def __init__(self, cdo: ICdoHandler, cache: ICacheHandler) -> None:
        self._cdo: ICdoHandler = cdo
        self._cache: ICacheHandler = cache

    def execute(
        self, commands: t.Tuple[str, ...], noutputs: int = 1
    ) -> t.Tuple[str, ...]:
        if not commands:
            raise ValueError("no commands provided")
        if noutputs < 1:
            raise ValueError("noutputs should be a positive integer")

        hash_code = self._cache.generate_hash(commands)

        cache_files = self._cache.generate_cache_paths(noutputs, hash_code)

        if not self._cache.cache_exists(cache_files):
            self._cdo.run((*commands, *cache_files))
            return cache_files

        input_files = self._cdo.get_input_files(commands)
        if input_files and not self._cache.is_cache_valid(cache_files, input_files):
            self._cdo.run((*commands, *cache_files))
        return cache_files
