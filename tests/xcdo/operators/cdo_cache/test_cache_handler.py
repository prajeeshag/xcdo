import pytest
import typing as t

from xcdo.operators.cdo_cache.exceptions import CacheError
from xcdo.operators.cdo_cache.interfaces import ICacheHandler
from xcdo.operators.cdo_cache.cache_handler import CacheHandler


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
        commands1 = ("-some", "-commands")
        commands2 = ("-some ", "-commands")
        result1 = cache_handler.generate_hash(commands1)
        result1c = cache_handler.generate_hash(commands1)
        result2 = cache_handler.generate_hash(commands2)

        assert isinstance(result1, str)
        assert isinstance(result2, str)

        assert result1 != result2
        assert result1 == result1c


class TestIsValidCache:
    def test_invalid_inputs(self, cache_handler: ICacheHandler):
        with pytest.raises(CacheError) as e:
            cache_handler.is_cache_valid((), ())
        assert str(e.value) == "no cache files provided"

    def test_no_input_files(self, cache_handler: ICacheHandler):
        input_files = ()
        cache_files = ("cache_file1", "cache_file2")
        result = cache_handler.is_cache_valid(cache_files, input_files)
        assert result is True


class TestCacheExists:
    def test_invalid_inputs(self, cache_handler: ICacheHandler):
        with pytest.raises(CacheError) as e:
            cache_handler.cache_exists(())
        assert str(e.value) == "no cache files provided"
