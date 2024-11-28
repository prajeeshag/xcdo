from xcdo import OperatorFns

from .missing_values import fn_registry as missing_value_registry
from .ploting import fn_registry as ploting_registry
from .renameing import fn_registry as renameing_registry
from .selecting import fn_registry as selecting_registry

fn_registry = OperatorFns()

fn_registry.update(selecting_registry)
fn_registry.update(ploting_registry)
fn_registry.update(missing_value_registry)
fn_registry.update(renameing_registry)
