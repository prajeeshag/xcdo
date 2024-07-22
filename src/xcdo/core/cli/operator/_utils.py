from typing import Any, Callable


def inspect_function(
    func: Callable[..., Any],
) -> tuple[list[tuple[str, type]], dict[str, type]]:
    return [], {}
