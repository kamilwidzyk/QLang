from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.operators import do_operation_add, do_operation_sub

if TYPE_CHECKING:
    from place import Place

def handle_add_sub(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles addition and subtraction operations
    ||| expr ('+' | '-') expr
    Calculations are performed using do_operation_add and do_operation_sub
    """
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    if operation == '+':
        return do_operation_add(left, right)
    if operation == '-':
        return do_operation_sub(left, right)
    