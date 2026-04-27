from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_number_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # NUMBER: FLOAT_NUMBER | HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;

    text = block.NUMBER().getText()
    val = None

    # parse text as hex(0x...), bin(0b...) or dec or float
    if text.startswith("0x") or text.startswith("0X"):
        val = int(text, 16)
    elif text.startswith("0b") or text.startswith("0B"):
        val = int(text, 2)
    elif "." in text or "e" in text or "E" in text:
        val = float(text)
    else:
        val = int(text)
    
    return val