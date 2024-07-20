import re

from .argument_token import AbstractTokenFactory, ArgumentToken


class LeftSquareBracket(ArgumentToken):
    pattern = re.compile(r"\[")


class RightSquareBracket(ArgumentToken):
    pattern = re.compile(r"\]")
