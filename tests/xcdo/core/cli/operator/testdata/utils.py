# type: ignore


def e_args(fn):
    res = []
    docstring = fn.__doc__.split("\n")
    res.append(docstring[1].strip())
    res.append(fn)
    if len(docstring) > 3:
        res.append(docstring[2].strip())
    return tuple(res)
