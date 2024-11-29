from clios import OperatorFns


def load_operator_registry() -> OperatorFns:
    from .operators import fn_registry
    from .operators import misc as misc
    from .operators import missing_values as missing_values
    from .operators import plotting as plotting
    from .operators import renaming as renaming
    from .operators import selecting as selecting

    return fn_registry
