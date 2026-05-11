from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.operators import do_operation_div
from ...operations.operators import do_operation_div_int
from ...operations.operators import do_operation_mod
from ...operations.operators import do_operation_mul
from ...expression import TYPE_INT, Expression

if TYPE_CHECKING:
    from place import Place

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('*' | '/' | '%') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    # TODO: Check types before the operation

    if operation == '*':
        return do_operation_mul(left, right)

    if operation == '/':
        if right == 0:
            self.script_errors.showError(pos, "RUNTIME ERROR", "Math Error","I don't do division by zero. Nobody does.")
            exit()

        if left.type == TYPE_INT and right.type == TYPE_INT:
            return do_operation_div_int(left, right)
        
        return do_operation_div(left, right)


    if operation == '%':
        if isinstance(left, str):
            # String formatting
            if isinstance(right, list):
                try:
                    return left % tuple(right)
                except:
                    return left % right
            else:
                return left % right
        else:
            # Numeric modulo
            if right == 0:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Math Error", "Modulo over zero? Bold of you to assume I'd allow that.")
                exit()
            return do_operation_mod(left, right)
