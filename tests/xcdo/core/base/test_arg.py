from xcdo.core.base.cli import Arg


def test_arg_strips_leading_spaces():
    value = "   leading spaces"
    arg = Arg(value)
    assert str(arg) == "leading spaces"


def test_arg_strips_trailing_spaces():
    value = "trailing spaces   "
    arg = Arg(value)
    assert str(arg) == "trailing spaces"


def test_arg_strips_leading_and_trailing_spaces():
    value = "   both leading and trailing   "
    arg = Arg(value)
    assert str(arg) == "both leading and trailing"


def test_arg_with_no_spaces():
    value = "no spaces"
    arg = Arg(value)
    assert str(arg) == "no spaces"
