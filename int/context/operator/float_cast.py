from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...operations.operators import do_operation_float_cast

if TYPE_CHECKING:
    from place import Place

def handle_float_cast(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles float cast operation
    ||| expr '.0'
    Calculation is performed using do_operation_float_cast
    """
    children = [x for x in block.getChildren()]
    # children[0] is the expr, children[1] is '.0'
    left = self.handle_block(children[0], block)

    return do_operation_float_cast(left, pos)
