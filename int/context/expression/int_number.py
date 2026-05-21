from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_INT

if TYPE_CHECKING:
    from place import Place

def handle_expression_int_number(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # INT_NUMBER: HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;

    text = block.INT_NUMBER().getText()
    val = None

    # parse text as hex(0x...), bin(0b...) or dec
    if text.startswith("0x") or text.startswith("0X"):
        val = int(text, 16)
    elif text.startswith("0b") or text.startswith("0B"):
        val = int(text, 2)
    else:
        val = int(text)
    
    return Expression(TYPE_INT, val)