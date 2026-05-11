from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.operators import do_operation_add, do_operation_sub

from ...exception.operator_type_mismatch import OperatorTypeMismatchException

if TYPE_CHECKING:
    from place import Place

def handle_add_sub(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('+' | '-') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    result = None

    # Handle string operations
    if isinstance(left, str) or isinstance(right, str):
        if operation == '+':
            return str(left) + str(right)
        elif operation == '-':
            # Remove all instances of characters in right from left
            if isinstance(right, str):
                for char in right:
                    left = str(left).replace(char, '')
                return left
            else:
                raise OperatorTypeMismatchException(
                    pos=pos,
                    left_type=type(left).__name__,
                    right_type=type(right).__name__,
                    operator=operation,
                    operator_worded="subtracting"
                )

    # Numeric operations
    if operation == '+':
        result = do_operation_add(left, right)
    elif operation == '-':
        result = do_operation_sub(left, right)

    return result