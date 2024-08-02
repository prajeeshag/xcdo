# type: ignore

import pytest
from xcdo.core.cli.operation import LeafOperation
from xcdo.core.cli.operator import Generator


@pytest.mark.parametrize(
    "args,kwargs,res",
    [
        [(), (), "s"],
        [("a", "1", "c"), (), 1],
        [("a", "1", "c"), (("k", "s"), ("l", "1")), 10.5],
    ],
)
def test_LeafOperationGenerator(mocker, args, kwargs, res):
    generator = mocker.Mock()
    op = LeafOperation(generator, args=args, kwargs=kwargs)
    generator.load_args.return_value = args
    generator.load_kwargs.return_value = dict(kwargs)
    generator.return_value = res
    isinstance_mock = mocker.patch("xcdo.core.cli.operation.isinstance")
    isinstance_mock.return_value = True
    result = op.execute()
    isinstance_mock.assert_called_once_with(generator, Generator)
    generator.load_args.assert_called_once_with(args)
    generator.load_kwargs.assert_called_once_with(dict(kwargs))
    generator.assert_called_once_with(*args, **dict(kwargs))
    assert result == res


@pytest.mark.parametrize(
    "filepath,res",
    [
        ["file1", "s"],
        ["file2", 1],
    ],
)
def test_LeafOperationReader(mocker, filepath, res):
    reader = mocker.Mock()
    op = LeafOperation(reader, args=(filepath,))
    reader.return_value = res
    isinstance_mock = mocker.patch("xcdo.core.cli.operation.isinstance")
    isinstance_mock.return_value = False
    result = op.execute()
    isinstance_mock.assert_called_once_with(reader, Generator)
    reader.assert_called_once_with(filepath)
    assert result == res
