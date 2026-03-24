from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('*' | '/' | '%') expr 

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "MulDivModExprContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) != 3:
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "MulDivModExprContext: 3 children expected")
        exit()
    
    val1 = self.handle_block(children[0], parent=block)
    val2 = self.handle_block(children[2], parent=block)

    if self.is_terminal(children[1], text='*', parent=block):
        return val1 * val2
    elif self.is_terminal(children[1], text='/', parent=block):
        if val2 == 0:
            self.script_errors.showError(pos, "RUNTIME ERROR", "Math Error", "I don't do division by zero. Nobody does.")
            exit()
        return val1 // val2
    elif self.is_terminal(children[1], text='%', parent=block):
        if val2 == 0:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Math Error", "Modulo over zero? Bold of you to assume I'd allow that.")
            exit()
        return val1 % val2
    else:
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "MulDivModExprContext: child index 1, expected '*', '/' or '%'")
        exit()