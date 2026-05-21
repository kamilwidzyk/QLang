from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_INT, TYPE_FLOAT

if TYPE_CHECKING:
    from place import Place

def handle_expression_number(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # NUMBER: FLOAT_NUMBER | HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;

    text = block.NUMBER().getText()
    val = None
    is_float = False

    # parse text as hex(0x...), bin(0b...) or dec or float
    if text.startswith("0x") or text.startswith("0X"):
        val = int(text, 16)
    elif text.startswith("0b") or text.startswith("0B"):
        val = int(text, 2)
    elif "." in text or "e" in text or "E" in text:
        val = float(text)
        is_float = True
    else:
        val = int(text)
    
    return Expression(TYPE_FLOAT if is_float else TYPE_INT, val)