from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_INT

if TYPE_CHECKING:
    from place import Place

from .common import parse_prefix_int


def handle_expression_int_number(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles integers in hexadecimal, binary and decimal formats
    ||| INT_NUMBER: HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;

    Hexadecimal:
        0xABC
        0XABC
    Binary:
        0b1100
        0B1100
    Decimal
        123
        456
    """
    text = block.INT_NUMBER().getText()
    return Expression(TYPE_INT, parse_prefix_int(text))