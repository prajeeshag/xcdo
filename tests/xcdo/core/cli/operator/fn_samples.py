# type: ignore


def fn1(
    i: int,
    f: float,
    s: str,
    b: bool,
    *args: float,
    ik: int = 1,
    fk: float | int = 0.1,
    sk: str = "str",
    bk: bool = False,
    **kwargs: int,
) -> None:
    pass


fn1_param = [
    fn1,
    (
        "fn1",
        [("i", int), ("f", float), ("s", str), ("b", bool), ("*args", float)],
        [
            ("ik", int, 1),
            ("fk", float | int, 0.1),
            ("sk", str, "str"),
            ("bk", bool, False),
            ("**kwargs", int, None),
        ],
        type(None),
    ),
]


def fn2(i, f, s, b, ik=1, *args, fk=0.1, sk="str", bk=False, **kwargs):
    pass


fn2_param = [
    fn2,
    (
        "fn2",
        [("i", None), ("f", None), ("s", None), ("b", None), ("*args", None)],
        [
            ("ik", None, 1),
            ("fk", None, 0.1),
            ("sk", None, "str"),
            ("bk", None, False),
            ("**kwargs", None, None),
        ],
        None,
    ),
]
