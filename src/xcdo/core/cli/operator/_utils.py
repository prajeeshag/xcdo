import inspect
from typing import Any, Callable, get_type_hints


def inspect_function(
    func: Callable[..., Any],
) -> tuple[
    str,
    list[tuple[str, Any]],
    list[tuple[str, Any, Any]],
    Any,
]:
    func_name = func.__name__
    # Get the signature of the function
    signature = inspect.signature(func)

    # Get the type hints of the function
    type_hints = get_type_hints(func)

    # Initialize the lists for args and kwargs
    args_types: list[tuple[str, Any]] = []
    kwargs_types: list[tuple[str, Any, Any]] = []

    for name, param in signature.parameters.items():
        param_type = type_hints.get(name, None)
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            args_types.append((f"*{name}", param_type))
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            kwargs_types.append((f"**{name}", param_type, None))
        elif param.default == inspect.Parameter.empty:
            args_types.append((name, param_type))
        else:
            kwargs_types.append((name, param_type, param.default))

    return_type = type_hints.get("return", None)

    return func_name, args_types, kwargs_types, return_type


def type2str(t: type) -> str:
    string = str(t).replace("<class '", "")
    string = string.replace("'>", "")
    return string
