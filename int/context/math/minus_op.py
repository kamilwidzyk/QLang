from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.operators import do_operation_minus

if TYPE_CHECKING:
    from place import Place

def handle_minus(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles unary minus operation
    ||| '-' expr
    Calculation is performed using do_operation_minus
    """
    val = self.handle_block(block.expr(), block)
    return do_operation_minus(val)