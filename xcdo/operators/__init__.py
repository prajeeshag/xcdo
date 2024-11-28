from xcdo import OperatorFns

from .plot import fn_registry as plot_registry
from .sel import fn_registry as sel_registry
from .setmiss import fn_registry as setmiss_registry

fn_registry = OperatorFns()

fn_registry.update(sel_registry)
fn_registry.update(plot_registry)
fn_registry.update(setmiss_registry)
