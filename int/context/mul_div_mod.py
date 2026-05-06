from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

from ..operations.operators import do_operation_mul, do_operation_div, do_operation_div_int, do_operation_mod

from ..exception.operator_type_mismatch import OperatorTypeMismatchException

if TYPE_CHECKING:
    from place import Place

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('*' | '/' | '%') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    result = None

    try:
        if operation == '*':
            result = do_operation_mul(left, right)
        elif operation == '/':
            if right == 0:
                self.script_errors.showError(pos, "RUNTIME ERROR", "Math Error","I don't do division by zero. Nobody does.")
                exit()
            # Check if both are integers for integer division
            if isinstance(left, int) and isinstance(right, int):
                result = do_operation_div_int(left, right)
            else:
                result = do_operation_div(left, right)
        elif operation == '%':
            if right == 0:
                parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
                self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Math Error", "Modulo over zero? Bold of you to assume I'd allow that.")
                exit()
            result = do_operation_mod(left, right)
    except TypeError:
        raise OperatorTypeMismatchException(
            pos=ScriptErrors.Position.extract(block),
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator=operation,
            operator_worded=
                {'*': "multiplying", "/": "dividing", "%": "taking modulo of"}.get(operation)
        )

    return result
