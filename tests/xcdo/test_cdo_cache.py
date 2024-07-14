from xcdo.cdo_cache import CdoCache, ICdoHandler, Utils
import pytest
from pytest_mock import MockerFixture, MockType
import typing as t


@pytest.fixture
def cdo_mock(mocker: MockerFixture):
    return mocker.MagicMock(spec=ICdoHandler)


@pytest.fixture
def utils_mock(mocker: MockerFixture):
    return mocker.MagicMock(spec=Utils)


@pytest.fixture
def cdo_cache(cdo_mock: MockType, utils_mock: MockType):
    return CdoCache(cdo_mock, utils_mock)


@pytest.fixture
def env(
    mocker: MockerFixture,
    cdo_mock: MockType,
    utils_mock: MockType,
    cdo_cache: CdoCache,
) -> t.Any:

    class Setup:
        def __init__(self):
            self.cdo_version = "x.x.x"
            self.hash_code = "xxxxxxxx"
            self.cdo_cache = cdo_cache
            self.utils_mock = utils_mock
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
            self.utils_mock.generate_hash.return_value = self.hash_code
            self.utils_mock.generate_cache_paths.return_value = self.cache_files
            self.utils_mock.cache_exists.return_value = cache_exist
            self.cdo_mock.get_input_files.return_value = input_files
            self.utils_mock.is_cache_valid.return_value = cache_valid
            self.utils_calls = []
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
    def test_return(self, env: t.Any, mocker: MockerFixture):
        self.arrange(env)  # type: ignore
        result = env.act()
        self.add_assert_calls(env, mocker)  # type: ignore
        assert env.utils_mock.method_calls == env.utils_calls
        assert env.cdo_mock.method_calls == env.cdo_calls
        assert result == env.cache_files


class CaseValidInputs:
    commands = ["-somecommand"]

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        env.utils_calls += [
            mocker.call.generate_hash(self.commands),
            mocker.call.generate_cache_paths(1, env.hash_code),
            mocker.call.cache_exists(env.cache_files),
        ]


class TestCacheDoesNotExists(CaseValidInputs, MixinTestReturn):
    def arrange(self, env: t.Any):
        env.arrange(commands=["-somecommand"], cache_exist=False)

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cdo_calls.append(mocker.call.run((*self.commands, *env.cache_files)))


class CaseCacheExists(CaseValidInputs):
    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cdo_calls.append(mocker.call.get_input_files(self.commands))


class TestNoInputFiles(CaseCacheExists, MixinTestReturn):

    def arrange(self, env: t.Any):
        env.arrange(commands=self.commands, cache_exist=True)


class CaseWithInputFiles(CaseCacheExists):
    input_files = ["some", "input", "files"]

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.utils_calls.append(
            mocker.call.is_cache_valid(env.cache_files, self.input_files)
        )


class TestCacheValid(CaseWithInputFiles, MixinTestReturn):

    def arrange(self, env: t.Any):
        env.arrange(
            commands=self.commands,
            cache_exist=True,
            input_files=self.input_files,
            cache_valid=True,
        )


class TestCacheNotValid(CaseWithInputFiles, MixinTestReturn):
    def arrange(self, env: t.Any):
        env.arrange(
            commands=self.commands,
            cache_exist=True,
            input_files=self.input_files,
            cache_valid=False,
        )

    def add_assert_calls(self, env: t.Any, mocker: MockerFixture):
        super().add_assert_calls(env, mocker)
        env.cdo_calls.append(mocker.call.run((*self.commands, *env.cache_files)))
