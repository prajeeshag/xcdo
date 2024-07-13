from xcdo import XCdo, ICdoHandler, _Utils  # type: ignore
import pytest
from pytest_mock import MockerFixture, MockType
import typing as t


@pytest.fixture
def cdo_mock(mocker: MockerFixture):
    return mocker.MagicMock(spec=ICdoHandler)


@pytest.fixture
def utils_mock(mocker: MockerFixture):
    return mocker.MagicMock(spec=_Utils)


@pytest.fixture
def xcdo(cdo_mock: MockType):
    return XCdo(cdo_mock)


@pytest.fixture
def setup_env(
    mocker: MockerFixture,
    cdo_mock: MockType,
    utils_mock: MockType,
    xcdo: XCdo,
) -> object:

    class Setup:
        def __init__(self):
            self.cdo_version = "x.x.x"
            self.hash_code = "xxxxxxxx"

        def prepare_mocks(
            self,
            input_files: t.List[str] = [],
            output_files: t.List[str] = [],
            commands: t.List[str] = [],
            all_cache_files_exist: bool = False,
            input_younger: bool = False,
            cache_linked: bool = False,
        ):
            self.input_files = input_files
            self.output_files = output_files
            self.cache_files = [self.hash_code + i for i in output_files]
            self.commands = commands
            self.iargv = self.commands + self.input_files
            self.argv = self.commands + self.input_files + self.output_files

            cdo_mock.get_output_files.return_value = self.output_files
            cdo_mock.version.return_value = self.cdo_version
            utils_mock.generate_hash.return_value = self.hash_code
            utils_mock.all_files_exist.return_value = all_cache_files_exist
            cdo_mock.get_input_files.return_value = self.input_files
            utils_mock.is_any_file_new.return_value = not input_younger
            utils_mock.are_all_linked_to.return_value = cache_linked

            mocker.patch("xcdo._Utils", return_value=utils_mock)
            mocker.patch.object(
                xcdo,
                "_generate_cache_file_paths",
                return_value=self.cache_files,
            )

            self.cdo_get_output_files_call = mocker.call.get_output_files(self.argv)
            self.cdo_version_call = mocker.call.version()
            self.cdo_get_input_files_call = mocker.call.get_input_files(
                self.argv,
                exclude_files=self.output_files,
            )
            self.cdo_run_call = mocker.call.run(self.argv)

            self.generate_hash_call = mocker.call.generate_hash(
                [*self.iargv, self.cdo_version]
            )
            self.cache_files_exist_call = mocker.call.all_files_exist(
                self.cache_files,
            )

            self.move_output_to_cache_call = mocker.call.move_all(
                list(zip(self.output_files, self.cache_files))
            )

            self.link_output_to_cache_call = mocker.call.link_all(
                list(zip(self.output_files, self.cache_files))
            )

            self.are_output_cache_linked_call = mocker.call.are_all_linked_to(
                list(zip(self.output_files, self.cache_files))
            )

            self.are_inputs_new_call = mocker.call.is_any_file_new(
                self.input_files, self.cache_files
            )

    return Setup()


def test_empty_argv(
    mocker: MockerFixture,
    cdo_mock: MockType,
    xcdo: XCdo,
):
    # Act
    xcdo([])

    # Assert
    assert cdo_mock.mock_calls == [mocker.call.run([])]


def test_no_output(
    mocker: MockerFixture,
    cdo_mock: MockType,
    xcdo: XCdo,
):
    # Arrange
    argv = "-some -arguments -without -output".split()
    cdo_mock.get_output_files.return_value = []

    # Act
    xcdo(argv)

    # Assert
    assert cdo_mock.mock_calls == [
        mocker.call.get_output_files(argv),
        mocker.call.run(argv),
    ]


class TestSingleOutputSingleInput:
    input_files = ["in.nc"]
    output_files = ["out.nc"]
    commands = "-some -commands".split()

    def test_cache_does_not_exist(
        self,
        setup_env: MockType,
        cdo_mock: MockType,
        utils_mock: MockType,
        xcdo: XCdo,
    ):
        # Arrange
        env = setup_env
        env.prepare_mocks(
            input_files=self.input_files,
            output_files=self.output_files,
            commands=self.commands,
        )

        # Act
        xcdo(env.argv)

        # Assert
        cdo_calls: t.List[t.Any] = []
        utils_calls: t.List[t.Any] = []
        cdo_calls.append(env.cdo_get_output_files_call)
        cdo_calls.append(env.cdo_version_call)
        utils_calls.append(env.generate_hash_call)
        utils_calls.append(env.cache_files_exist_call)
        cdo_calls.append(env.cdo_run_call)
        utils_calls.append(env.move_output_to_cache_call)
        utils_calls.append(env.link_output_to_cache_call)

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls

    def test_cache_exist_but_input_file_younger(
        self,
        setup_env: MockType,
        cdo_mock: MockType,
        utils_mock: MockType,
        xcdo: XCdo,
    ):
        # Arrange
        env = setup_env
        env.prepare_mocks(
            input_files=self.input_files,
            output_files=self.output_files,
            commands=self.commands,
            all_cache_files_exist=True,
            input_younger=True,
        )

        # Act
        xcdo(env.argv)

        # Assert
        cdo_calls: t.List[t.Any] = []
        utils_calls: t.List[t.Any] = []
        cdo_calls.append(env.cdo_get_output_files_call)
        cdo_calls.append(env.cdo_version_call)
        utils_calls.append(env.generate_hash_call)
        utils_calls.append(env.cache_files_exist_call)
        cdo_calls.append(env.cdo_get_input_files_call)
        utils_calls.append(env.are_inputs_new_call)
        cdo_calls.append(env.cdo_run_call)
        utils_calls.append(env.move_output_to_cache_call)
        utils_calls.append(env.link_output_to_cache_call)

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls

    def test_cache_exist_and_input_file_older_and_cache_linked(
        self,
        setup_env: MockType,
        cdo_mock: MockType,
        utils_mock: MockType,
        xcdo: XCdo,
    ):
        # Arrange
        env = setup_env
        env.prepare_mocks(
            input_files=self.input_files,
            output_files=self.output_files,
            commands=self.commands,
            all_cache_files_exist=True,
            input_younger=False,
            cache_linked=True,
        )

        # Act
        xcdo(env.argv)

        # Assert
        cdo_calls: t.List[t.Any] = []
        utils_calls: t.List[t.Any] = []
        cdo_calls.append(env.cdo_get_output_files_call)
        cdo_calls.append(env.cdo_version_call)
        utils_calls.append(env.generate_hash_call)
        utils_calls.append(env.cache_files_exist_call)
        cdo_calls.append(env.cdo_get_input_files_call)
        utils_calls.append(env.are_inputs_new_call)
        utils_calls.append(env.are_output_cache_linked_call)

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls

    def test_cache_exist_and_input_files_older_and_cache_not_linked(
        self,
        setup_env: MockType,
        cdo_mock: MockType,
        utils_mock: MockType,
        xcdo: XCdo,
    ):
        # Arrange
        env = setup_env
        env.prepare_mocks(
            input_files=self.input_files,
            output_files=self.output_files,
            commands=self.commands,
            all_cache_files_exist=True,
            input_younger=False,
            cache_linked=False,
        )

        # Act
        xcdo(env.argv)

        # Assert
        cdo_calls: t.List[t.Any] = []
        utils_calls: t.Any = []
        cdo_calls.append(env.cdo_get_output_files_call)
        cdo_calls.append(env.cdo_version_call)
        utils_calls.append(env.generate_hash_call)
        utils_calls.append(env.cache_files_exist_call)
        cdo_calls.append(env.cdo_get_input_files_call)
        utils_calls.append(env.are_inputs_new_call)
        utils_calls.append(env.are_output_cache_linked_call)
        utils_calls.append(env.link_output_to_cache_call)

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls


class TestSingleOutputMultipleInput(TestSingleOutputSingleInput):
    input_files = ["in1.nc", "in2.nc", "in3.nc"]


class TestMulitpleOutputSingleInput(TestSingleOutputSingleInput):
    output_files = ["o1.nc", "o2.nc", "o3.nc"]


class TestMulitpleOutputMultipleInput(TestSingleOutputSingleInput):
    input_files = ["in1.nc", "in2.nc", "in3.nc"]
    output_files = ["o1.nc", "o2.nc", "o3.nc"]


class TestSingleOutputNoInput(TestSingleOutputMultipleInput):
    input_files = []
