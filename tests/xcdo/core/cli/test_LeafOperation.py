# type: ignore

import pytest
from pytest_mock import MockerFixture
from xcdo.core.cli.operation import LeafOperation


@pytest.mark.parametrize(
    "args,kwargs,res",
    [
        [(), (), "s"],
        [("a", "1", "c"), (), 1],
        [("a", "1", "c"), (("k", "s"), ("l", "1")), 10.5],
    ],
)
def test_LeafOperationGenerator(mocker: MockerFixture, args, kwargs, res):
    generator = mocker.patch(
        "xcdo.core.cli.operator.Generator", autospec=True
    ).return_value
    generator.load_args.return_value = args
    generator.load_kwargs.return_value = dict(kwargs)
    generator.return_value = res

    op = LeafOperation(generator, args=args, kwargs=kwargs)
    result = op.execute()
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
    reader = mocker.patch("xcdo.core.cli.operator.Reader", autospec=True).return_value
    op = LeafOperation(reader, args=(filepath,))
    reader.return_value = res
    result = op.execute()
    reader.assert_called_once_with(filepath)
    assert result == res
