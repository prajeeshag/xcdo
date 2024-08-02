# type: ignore

import pytest
from xcdo.core.cli.operation import WriterOperation


@pytest.mark.parametrize(
    "filepaths,input",
    [
        [(), "s"],
        [("file1",), "s"],
        [("file1", "file2"), 1],
    ],
)
def test_WriterOperation(mocker, filepaths, input):
    writer = mocker.patch("xcdo.core.cli.operator.Writer", autospec=True).return_value
    child_op = mocker.Mock()
    child_op.execute.return_value = input
    op = WriterOperation(writer, child_op, filepaths)
    op.execute()
    child_op.execute.assert_called_once()
    writer.assert_called_once_with(input, *filepaths)
