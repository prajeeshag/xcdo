from xcdo.core.base.arg import Arg


def test_arg_strips_leading_spaces():
    value = "   leading spaces"
    arg = Arg(value)
    assert arg == "leading spaces"


def test_arg_strips_trailing_spaces():
    value = "trailing spaces   "
    arg = Arg(value)
    assert arg == "trailing spaces"


def test_arg_strips_leading_and_trailing_spaces():
    value = "   both leading and trailing   "
    arg = Arg(value)
    assert arg == "both leading and trailing"


def test_arg_with_no_spaces():
    value = "no spaces"
    arg = Arg(value)
    assert arg == "no spaces"


def test_arg_is_instance_of_str():
    value = "   instance test   "
    arg = Arg(value)
    assert isinstance(arg, str)


def test_arg_is_instance_of_arg():
    value = "   instance test   "
    arg = Arg(value)
    assert isinstance(arg, Arg)
