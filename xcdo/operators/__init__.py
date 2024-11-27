from xcdo import OperatorFns

from ._plot import fn_registry as plot_registry
from ._sel import fn_registry as sel_registry

fn_registry = OperatorFns()

fn_registry.update(sel_registry)
fn_registry.update(plot_registry)
