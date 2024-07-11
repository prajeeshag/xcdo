import unittest
from unittest.mock import MagicMock, call, patch, DEFAULT
import tempfile


from xcdo import XCdo, ICdoHandler
import xcdo


class TestXCdoCallSuccess(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_cdo = MagicMock(spec=ICdoHandler)
        self.obj = XCdo(self.mock_cdo)
        #    self.hash_code = "abcdef123456"
        #    self.output_files = [
        #        "/home/user/projects/file1.txt",
        #        "/home/user/projects/file2.txt",
        #    ]
        #    # self.cachedir_name = self.xcdo._cachedir_name
        #    self.helper_options_ = [
        #        "--dryrun",
        #        "-A",
        #        "--help",
        #        "-h",
        #        "--apply",
        #        "--argument_groups",
        #    ]
        return super().setUp()

    def test_with_empty_argv(self):
        # Arrange

        # Act
        self.obj([])

        # Assert
        self.mock_cdo.run.assert_called_once_with([])
        self.assertEqual(
            self.mock_cdo.method_calls, [call.run([])], "Should only call run"
        )

    def test_no_output(self, **mocks):
        # Arrange
        argv = "-some -arguments -without -output".split()
        self.mock_cdo.get_output_files.return_value = []

        # Act
        self.obj(argv)

        # Assert
        self.mock_cdo.get_output_files.assert_called_once_with(argv)
        self.mock_cdo.run.assert_called_once_with(argv)
        self.assertEqual(
            self.mock_cdo.method_calls,
            [call.get_output_files(argv), call.run(argv)],
        )

    @patch.multiple(
        "xcdo",
        _generate_hash=DEFAULT,
        _mv_and_link_back=DEFAULT,
    )
    def test_single_output_in_cwd(self, **mocks):
        # Arrange
        out_file = "out.nc"
        iargv = "-some -operators ".split()
        argv = iargv + [out_file]
        cdo_version = "x.x.x"
        hash_code = "xxxxxxxx"
        cache_file = f"{XCdo._cachedir_name}/{hash_code}"
        self.mock_cdo.get_output_files.return_value = [out_file]
        self.mock_cdo.version.return_value = cdo_version
        mocks["_generate_hash"].return_value = hash_code

        # Act
        self.obj(argv)

        # Assert
        self.mock_cdo.get_output_files.assert_called_once_with(argv)
        self.mock_cdo.version.assert_called_once_with()
        mocks["_generate_hash"].assert_called_once_with([*iargv, cdo_version])
        self.mock_cdo.run.assert_called_once_with(argv)
        mocks["_mv_and_link_back"].assert_called_once_with(out_file, cache_file)

    @patch.multiple(
        "xcdo",
        _generate_hash=DEFAULT,
        _mv_and_link_back=DEFAULT,
    )
    def test_multiple_output_in_cwd(self, **mocks):
        # Arrange
        hash_code = "xxxxxxxx"
        out_files = "o1.nc o2.nc o3.nc".split()
        iargv = "-some -operators ".split()
        argv = iargv + out_files
        cdo_version = "x.x.x"
        cache_files = (
            f"{XCdo._cachedir_name}/0_{hash_code}"
            + f"{XCdo._cachedir_name}/1_{hash_code}"
            + f"{XCdo._cachedir_name}/2_{hash_code}".split()
        )
        self.mock_cdo.get_output_files.return_value = out_files
        self.mock_cdo.version.return_value = cdo_version
        mocks["_generate_hash"].return_value = hash_code

        # Act
        self.obj(argv)

        # Assert
        self.mock_cdo.get_output_files.assert_called_once_with(argv)
        self.mock_cdo.version.assert_called_once_with()
        mocks["_generate_hash"].assert_called_once_with([*iargv, cdo_version])
        self.mock_cdo.run.assert_called_once_with(argv)
        mocks["_mv_and_link_back"].assert_called_once_with(out_file, cache_file)

    # def test__get_input_files(self):
    #     with (
    #         tempfile.NamedTemporaryFile() as file1,
    #         tempfile.NamedTemporaryFile() as file2,
    #     ):
    #         argc = f"-sub [-timmean {file1.name} ] -remapbil,{file1.name} {file2.name}"
    #         argsv = argc.split()
    #         self.assertEqual(
    #             self.xcdo._get_input_files(argsv),
    #             {file1.name, file2.name},
    #         )
    #     self.assertEqual(
    #         self.xcdo._get_input_files(argsv),
    #         set(),
    #     )

    # def test__get_output_files(self):
    #     argsv = "-f nc -subc,9.0 -timmean i1 o1".split()
    #     self.assertEqual(
    #         self.xcdo._get_output_files(argsv),
    #         (argsv[-1],),
    #         "Should work for operators with one output",
    #     )

    #     argsv = "-f nc -trend i1 o1 o2".split()
    #     self.assertEqual(
    #         self.xcdo._get_output_files(argsv),
    #         (argsv[-2], argsv[-1]),
    #         "Should work for operators with 2 outputs",
    #     )

    #     self.assertEqual(
    #         self.xcdo._get_output_files(argsv),
    #         (tuple(argsv[-2:])),
    #         "Should return in same order",
    #     )

    #     argsv = "-f nc -output -timmean i1".split()
    #     self.assertEqual(
    #         self.xcdo._get_output_files(argsv),
    #         (),
    #         "Should work for operators with no outputs",
    #     )

    #     argsv = "-f nc output -timmean i1".split()
    #     self.assertEqual(
    #         self.xcdo._get_output_files(argsv),
    #         (),
    #         "Should work for non-dashed-no-output-operators",
    #     )

    #     for opt in [
    #         "--dryrun",
    #         "-A",
    #         "--help",
    #         "-h",
    #         "--apply",
    #         "--argument_groups",
    #     ]:
    #         argsv = f"{opt} -f nc -output -timmean i1".split()
    #         self.assertEqual(
    #             self.xcdo._get_output_files(argsv),
    #             (),
    #             f"Should return empty if input contains '{opt}'",
    #         )

    # def test__generate_hash(self):
    #     argsv1 = "-subc,9.0 -remapbil,grid.nc input.nc output.nc".split()
    #     argsv2 = "-subc,9.0 -remapbil ,grid.nc input .nc output.nc".split()
    #     self.assertEqual(
    #         self.xcdo._generate_hash(argsv1),
    #         self.xcdo._generate_hash(argsv1),
    #         "Hashes should be consistent for the same input",
    #     )
    #     self.assertNotEqual(
    #         self.xcdo._generate_hash(argsv1),
    #         self.xcdo._generate_hash(argsv2),
    #         "Hashes should be different for different input",
    #     )

    # def test_generate_cache_file_paths(self):
    #     expected = {
    #         "/home/user/projects/file1.txt": f"/home/user/projects/{self.cachedir_name}/0_abcdef123456",
    #         "/home/user/projects/file2.txt": f"/home/user/projects/{self.cachedir_name}/1_abcdef123456",
    #     }

    #     result = self.xcdo._generate_cache_file_paths(self.hash_code, self.output_files)
    #     self.assertEqual(result, expected, "Should work for multiple files")

    #     expected = {}
    #     result = self.xcdo._generate_cache_file_paths(self.hash_code, [])
    #     self.assertEqual(result, expected, "Should work for no files")

    #     single_output_file = ["/home/user/projects/file1.txt"]
    #     expected = {
    #         "/home/user/projects/file1.txt": f"/home/user/projects/{self.cachedir_name}/0_abcdef123456"
    #     }
    #     result = self.xcdo._generate_cache_file_paths(
    #         self.hash_code, single_output_file
    #     )
    #     self.assertEqual(result, expected, "Should work for single file")


if __name__ == "__main__":
    unittest.main()
