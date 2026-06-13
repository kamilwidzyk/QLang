from typing import Any, TYPE_CHECKING

from ...operations.operators import do_operation_bits_to_int, do_operation_int_to_bits
from ...script_errors import ScriptErrors

from ...exception.unsupported_conversion_type import UnsupportedConversionTypeException

if TYPE_CHECKING:
    from place import Place


def handle_binary_from_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles binary conversion from list to num only
    ||| expr '>>' varType
    Calculation is performed using do_operation_bits_to_int
    """
    left_expr = self.handle_block(block.expr(), block)
    target_type = block.varType().getText()

    if target_type != "num":
        # code UCT-1
        raise UnsupportedConversionTypeException(
            ScriptErrors.Position.extract(block.varType()), target_type, code="1")

    return do_operation_bits_to_int(left_expr, pos)


def handle_binary_to_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles binary conversion from num to list only(fixed bit width)
    ||| expr '>' INT_NUMBER '>' varType
    Calculation is performed using do_operation_int_to_bits
    """
    left_expr = self.handle_block(block.expr(), block)
    size_text = block.INT_NUMBER().getText()
    target_type = block.varType().getText()

    if target_type != "obs":
        # code UCT-1
        raise UnsupportedConversionTypeException(
            ScriptErrors.Position.extract(block.varType()), target_type, code="1")

    try:
        size = int(size_text, 0)
    except ValueError:
        raise TypeError("Invalid bit width for binary conversion")

    return do_operation_int_to_bits(left_expr, size, pos)
