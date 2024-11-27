from clios import OperatorFns


def load_operator_registry() -> OperatorFns:
    from .operators import fn_registry

    return fn_registry
