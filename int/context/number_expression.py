from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_number_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # numerical expression
    # TODO: there will be more, not it's just a Terminal number
    #print("Parsing numExprContext")

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "numExprContext: 'children' key missing or no children")
        exit()

    val = None

    for child in block["children"]:
        # terminal -> just a numebr
        if self.is_type(child, type=TERMINAL, parent=block):
            text = self.extract_text(child, parent=block)
            # parse text as hex(0x...), bin(0b...) or dec
            if text.startswith("0x") or text.startswith("0X"):
                val = int(text, 16)
            elif text.startswith("0b") or text.startswith("0B"):
                val = int(text, 2)
            else:
                val = int(text)
    
    #print("Parsing done, value: " + str(val))
    return val