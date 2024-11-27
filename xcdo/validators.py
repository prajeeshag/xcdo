import typing as t
from pathlib import Path

from .utils import open_dataset


def input_file_validator(path: str) -> str:
    assert Path(path).exists(), f"File {path} does not exist"
    return path


def path_to_dataset_validator(path: t.Any) -> t.Any:
    if isinstance(path, str):
        return open_dataset(path)
    return path


def output_file_validator(path: str) -> str:
    parent = Path(path).parent
    assert parent.exists(), f"Directory {parent} does not exist"
    return path
