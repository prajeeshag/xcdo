from xcdo import XCdo, ICdoHandler, _Utils
import pytest


@pytest.fixture
def cdo_mock(mocker):
    return mocker.MagicMock(spec=ICdoHandler)


@pytest.fixture
def utils_mock(mocker):
    return mocker.MagicMock(spec=_Utils)


@pytest.fixture
def xcdo(cdo_mock):
    return XCdo(cdo_mock)


def test_empty_argv(mocker, cdo_mock, xcdo):
    # Act
    xcdo([])

    # Assert
    assert cdo_mock.mock_calls == [mocker.call.run([])]


def test_no_output(mocker, cdo_mock, xcdo):
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


class TestSingleOutput:
    out_file = "o1.nc"
    input_files = "i1.nc i2.nc i3.nc".split()
    cache_file = "xxxxxxxxxxx1"
    cdo_version = "x.x.x"
    hash_code = "xxxxxxxx"
    iargv = "-some -operators ".split()

    def test_cache_does_not_exist(self, mocker, cdo_mock, utils_mock, xcdo):
        # Arrange
        argv = self.iargv + [self.out_file]
        cdo_mock.get_output_files.return_value = [self.out_file]
        cdo_mock.version.return_value = self.cdo_version
        utils_mock.generate_hash.return_value = self.hash_code
        utils_mock.file_exists.return_value = False
        mocker.patch("xcdo._Utils", return_value=utils_mock)
        mocker.patch.object(
            xcdo,
            "_generate_cache_file_paths",
            return_value={self.out_file: self.cache_file},
        )

        # Act
        xcdo(argv)

        # Assert
        cdo_calls = []
        utils_calls = []

        cdo_calls.append(mocker.call.get_output_files(argv))
        cdo_calls.append(mocker.call.version())
        utils_calls.append(mocker.call.generate_hash([*self.iargv, self.cdo_version]))
        utils_calls.append(mocker.call.file_exists(self.cache_file))
        cdo_calls.append(mocker.call.run(argv))
        utils_calls.append(mocker.call.move(self.out_file, self.cache_file))
        utils_calls.append(mocker.call.symlink_to(self.out_file, self.cache_file))

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls

    def test_cache_exist_but_input_files_younger(
        self, mocker, cdo_mock, utils_mock, xcdo
    ):
        # Arrange
        argv = self.iargv + [self.out_file]
        cdo_mock.get_output_files.return_value = [self.out_file]
        cdo_mock.version.return_value = self.cdo_version
        utils_mock.generate_hash.return_value = self.hash_code
        utils_mock.file_exists.return_value = True
        cdo_mock.get_input_files.return_value = self.input_files
        utils_mock.are_older_than.return_value = False
        utils_mock.is_symlink_to.return_value = False

        mocker.patch("xcdo._Utils", return_value=utils_mock)
        mocker.patch.object(
            xcdo,
            "_generate_cache_file_paths",
            return_value={self.out_file: self.cache_file},
        )

        # Act
        xcdo(argv)

        # Assert
        cdo_calls = []
        utils_calls = []

        cdo_calls.append(mocker.call.get_output_files(argv))
        cdo_calls.append(mocker.call.version())
        utils_calls.append(mocker.call.generate_hash([*self.iargv, self.cdo_version]))
        utils_calls.append(mocker.call.file_exists(self.cache_file))
        cdo_calls.append(
            mocker.call.get_input_files(argv, exclude_files=[self.out_file])
        )
        utils_calls.append(
            mocker.call.are_older_than(self.input_files, [self.out_file])
        )
        cdo_calls.append(mocker.call.run(argv))
        utils_calls.append(mocker.call.move(self.out_file, self.cache_file))
        utils_calls.append(mocker.call.symlink_to(self.out_file, self.cache_file))

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls

    def test_cache_exist_and_input_files_older_and_cache_linked(
        self, mocker, cdo_mock, utils_mock, xcdo
    ):
        # Arrange
        argv = self.iargv + [self.out_file]
        cdo_mock.get_output_files.return_value = [self.out_file]
        cdo_mock.version.return_value = self.cdo_version
        utils_mock.generate_hash.return_value = self.hash_code
        utils_mock.file_exists.return_value = True
        cdo_mock.get_input_files.return_value = self.input_files
        utils_mock.are_older_than.return_value = True
        utils_mock.is_symlink_to.return_value = True

        mocker.patch("xcdo._Utils", return_value=utils_mock)
        mocker.patch.object(
            xcdo,
            "_generate_cache_file_paths",
            return_value={self.out_file: self.cache_file},
        )

        # Act
        xcdo(argv)

        # Assert
        cdo_calls = []
        utils_calls = []

        cdo_calls.append(mocker.call.get_output_files(argv))
        cdo_calls.append(mocker.call.version())
        utils_calls.append(mocker.call.generate_hash([*self.iargv, self.cdo_version]))
        utils_calls.append(mocker.call.file_exists(self.cache_file))
        cdo_calls.append(
            mocker.call.get_input_files(argv, exclude_files=[self.out_file])
        )
        utils_calls.append(
            mocker.call.are_older_than(self.input_files, [self.out_file])
        )
        utils_calls.append(mocker.call.is_symlink_to(self.out_file, self.cache_file))

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls

    def test_cache_exist_and_input_files_older_and_cache_not_linked(
        self, mocker, cdo_mock, utils_mock, xcdo
    ):
        # Arrange
        argv = self.iargv + [self.out_file]
        cdo_mock.get_output_files.return_value = [self.out_file]
        cdo_mock.version.return_value = self.cdo_version
        utils_mock.generate_hash.return_value = self.hash_code
        utils_mock.file_exists.return_value = True
        cdo_mock.get_input_files.return_value = self.input_files
        utils_mock.are_older_than.return_value = True
        utils_mock.is_symlink_to.return_value = False

        mocker.patch("xcdo._Utils", return_value=utils_mock)
        mocker.patch.object(
            xcdo,
            "_generate_cache_file_paths",
            return_value={self.out_file: self.cache_file},
        )

        # Act
        xcdo(argv)

        # Assert
        cdo_calls = []
        utils_calls = []

        cdo_calls.append(mocker.call.get_output_files(argv))
        cdo_calls.append(mocker.call.version())
        utils_calls.append(mocker.call.generate_hash([*self.iargv, self.cdo_version]))
        utils_calls.append(mocker.call.file_exists(self.cache_file))
        cdo_calls.append(
            mocker.call.get_input_files(argv, exclude_files=[self.out_file])
        )
        utils_calls.append(
            mocker.call.are_older_than(self.input_files, [self.out_file])
        )
        utils_calls.append(mocker.call.is_symlink_to(self.out_file, self.cache_file))
        utils_calls.append(mocker.call.symlink_to(self.out_file, self.cache_file))

        assert cdo_mock.mock_calls == cdo_calls
        assert utils_mock.mock_calls == utils_calls
