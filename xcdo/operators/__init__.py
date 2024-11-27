from xcdo import OperatorFns

from ._sel import fn_registry as sel_registry

fn_registry = OperatorFns()

fn_registry.update(sel_registry)
