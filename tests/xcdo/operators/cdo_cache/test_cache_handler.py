from pathlib import Path
import pytest
import typing as t

from xcdo.operators.cdo_cache.exceptions import CacheError
from xcdo.operators.cdo_cache.interfaces import ICacheHandler
from xcdo.operators.cdo_cache.cache_handler import CacheHandler

from ._utils import randomcmd, randomfile, randomword


@pytest.fixture
def cache_handler():
    return CacheHandler()


def test_correct_instance(cache_handler: ICacheHandler):
    assert isinstance(cache_handler, ICacheHandler)


class TestGenerateHash:
    def test_invalid_inputs(self, cache_handler: t.Any):
        with pytest.raises(CacheError) as e:
            cache_handler.generate_hash([])

        assert str(e.value) == "empty commands"

    def test_valid_commands(self, cache_handler: t.Any):
        commands1 = (randomcmd(), randomcmd())
        commands2 = (randomcmd(), randomcmd())
        result1 = cache_handler.generate_hash(commands1)
        result1c = cache_handler.generate_hash(commands1)
        result2 = cache_handler.generate_hash(commands2)

        assert isinstance(result1, str)
        assert isinstance(result2, str)

        assert result1 != result2
        assert result1 == result1c


class Test_is_valid_cache:
    def test_empty_inputs(self, cache_handler: ICacheHandler):
        with pytest.raises(CacheError) as e:
            cache_handler.is_cache_valid((), ())
        assert str(e.value) == "no cache files provided"

    def test_empty_input_files_nonexistent_cache_files(
        self,
        cache_handler: ICacheHandler,
        tmp_path: Path,
    ):
        input_files = ()
        cache_files = [str(randomfile(tmp_path)) for _ in range(3)]
        result = cache_handler.is_cache_valid(cache_files, input_files)
        assert result is False

    def test_empty_input_files_existing_cache_files(
        self,
        cache_handler: ICacheHandler,
        tmp_path: Path,
    ):
        input_files = ()
        cache_files = [randomfile(tmp_path) for _ in range(3)]
        [f.write_text(" ") for f in cache_files]
        cache_files = list(map(str, cache_files))
        result = cache_handler.is_cache_valid(cache_files, input_files)
        assert result is True


class TestCacheExists:
    def test_invalid_inputs(self, cache_handler: ICacheHandler):
        with pytest.raises(CacheError) as e:
            cache_handler.cache_exists(())
        assert str(e.value) == "no cache files provided"
