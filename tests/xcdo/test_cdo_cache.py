from xcdo.operators.cdo_cache.interfaces import ICdoHandler, ICacheHandler
from xcdo.operators.cdo_cache import CdoCache

import pytest
from pytest_mock import MockerFixture, MockType
import typing as t


@pytest.fixture
def cdo_mock(mocker: MockerFixture):
    return mocker.MagicMock(spec=ICdoHandler)


@pytest.fixture
def cache_mock(mocker: MockerFixture):
    return mocker.MagicMock(spec=ICacheHandler)


@pytest.fixture
def cdo_cache(cdo_mock: MockType, cache_mock: MockType):
    return CdoCache(cdo_mock, cache_mock)


@pytest.fixture
def env(
    mocker: MockerFixture,
    cdo_mock: MockType,
    cache_mock: MockType,
    cdo_cache: CdoCache,
) -> t.Any:

    class Setup:
        def __init__(self):
            self.cdo_version = "x.x.x"
            self.hash_code = "xxxxxxxx"
            self.cdo_cache = cdo_cache
            self.cache_mock = cache_mock
            self.cdo_mock = cdo_mock
            self.input_files = ["some", "input", "files"]

        def arrange(
            self,
            commands: t.Tuple[str, ...] = (),
            noutputs: int | None = None,
            input_files: t.List[str] = [],
            cache_exist: bool = False,
            cache_valid: bool = False,
        ):
            self.input_files = input_files
            self.commands = commands
            self.noutputs = noutputs
            self.cache_files = [
                f"{self.hash_code}{n}" for n in range(noutputs if noutputs else 1)
            ]
            self.cache_mock.generate_hash.return_value = self.hash_code
            self.cache_mock.generate_cache_paths.return_value = self.cache_files
            self.cache_mock.cache_exists.return_value = cache_exist
            self.cdo_mock.get_input_files.return_value = input_files
            self.cdo_mock.version.return_value = self.cdo_version
            self.cache_mock.is_cache_valid.return_value = cache_valid
            self.cache_calls = []
            self.cdo_calls = []

        def act(self):
            if self.noutputs is None:
                return self.cdo_cache.execute(self.commands)

            return self.cdo_cache.execute(self.commands, self.noutputs)

    return Setup()


def test_no_command(env: t.Any):
    env.arrange()

    with pytest.raises(ValueError) as result:
        env.act()

    assert str(result.value) == "no commands provided"


@pytest.mark.parametrize("noutputs", [0, -1, -3])
def test_noutputs_not_positive_integer(env: t.Any, noutputs: int):
    env.arrange(commands=["-somecommand"], noutputs=noutputs)

    with pytest.raises(ValueError) as result:
        env.act()

    assert str(result.value) == "noutputs should be a positive integer"


class MixinTestReturn:
    @pytest.mark.parametrize("commands", [("-somecommand",), ("-some", "-command")])
    @pytest.mark.parametrize("noutputs", [None, 1, 2, 3])
    def test_return(
        self,
        env: t.Any,
        mocker: MockerFixture,
        noutputs: int,
        commands: t.Tuple[str, ...],
    ):
        self.arrange(env, noutputs=noutputs, commands=commands)  # type: ignore
        result = env.act()
        self.add_assert_calls(env, mocker)  # type: ignore
        assert env.cache_mock.method_calls == env.cache_calls
        assert env.cdo_mock.method_calls == env.cdo_calls
        assert result == env.cache_files


class CaseValidInputs:

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        env.cache_calls += [
            mocker.call.generate_hash(
                (*env.commands, env.cdo_version, *env.input_files)
            ),
            mocker.call.generate_cache_paths(
                env.noutputs if env.noutputs is not None else 1, env.hash_code
            ),
            mocker.call.cache_exists(env.cache_files),
        ]
        env.cdo_calls += [
            mocker.call.version(),
            mocker.call.get_input_files(env.commands),
        ]


class TestCacheDoesNotExists(CaseValidInputs, MixinTestReturn):
    def arrange(self, env: t.Any, **kwargs: t.Dict[str, t.Any]):
        env.arrange(cache_exist=False, **kwargs)

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cdo_calls.append(mocker.call.run((*env.commands, *env.cache_files)))


class CaseCacheExists(CaseValidInputs):
    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)


class TestNoInputFiles(CaseCacheExists, MixinTestReturn):

    def arrange(self, env: t.Any, **kwargs: t.Any):
        env.arrange(cache_exist=True, **kwargs)


class CaseWithInputFiles(CaseCacheExists):

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cache_calls.append(
            mocker.call.is_cache_valid(
                env.cache_files,
                self.input_files,  # type: ignore
            )
        )


class TestCacheValidSingleInputFile(CaseWithInputFiles, MixinTestReturn):
    input_files = ["someinputfiles"]

    def arrange(self, env: t.Any, **kwargs: t.Any):
        env.arrange(
            cache_exist=True,
            input_files=self.input_files,
            cache_valid=True,
            **kwargs,
        )


class TestCacheNotValidSingleInputFile(CaseWithInputFiles, MixinTestReturn):
    input_files = ["someinputfiles"]

    def arrange(self, env: t.Any, **kwargs: t.Any):
        env.arrange(
            cache_exist=True,
            input_files=self.input_files,
            cache_valid=False,
            **kwargs,
        )

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cdo_calls.append(mocker.call.run((*env.commands, *env.cache_files)))


class TestCacheValidMultipleInputFile(CaseWithInputFiles, MixinTestReturn):
    input_files = ["some", "input", "files"]

    def arrange(self, env: t.Any, **kwargs: t.Any):
        env.arrange(
            cache_exist=True,
            input_files=self.input_files,
            cache_valid=True,
            **kwargs,
        )


class TestCacheNotValidMultpleInputFile(CaseWithInputFiles, MixinTestReturn):
    input_files = ["some", "input", "files"]

    def arrange(self, env: t.Any, **kwargs: t.Any):
        env.arrange(
            cache_exist=True,
            input_files=self.input_files,
            cache_valid=False,
            **kwargs,
        )

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cdo_calls.append(mocker.call.run((*env.commands, *env.cache_files)))
