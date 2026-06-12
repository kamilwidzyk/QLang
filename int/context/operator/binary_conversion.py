from typing import Any, TYPE_CHECKING

from ...expression import Expression, TYPE_INT, TYPE_LIST, TYPE_OBS
from ...operations.operators import do_operation_bits_to_int, do_operation_int_to_bits
from ...script_errors import ScriptErrors

if TYPE_CHECKING:
    from place import Place


def handle_binary_from_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '>>' varType
    left_expr = self.handle_block(block.expr(), block)
    target_type = block.varType().getText()

    if target_type != "num":
        raise TypeError("Binary conversion to num only supports '>> num'")

    return do_operation_bits_to_int(left_expr)


def handle_binary_to_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '>' INT_NUMBER '>' varType
    left_expr = self.handle_block(block.expr(), block)
    size_text = block.INT_NUMBER().getText()
    target_type = block.varType().getText()

    if target_type != "obs":
        raise TypeError("Binary conversion to obs only supports '>N> obs'")

    try:
        size = int(size_text, 0)
    except ValueError:
        raise TypeError("Invalid bit width for binary conversion")

    return do_operation_int_to_bits(left_expr, size)
