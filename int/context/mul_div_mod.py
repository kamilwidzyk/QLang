from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('*' | '/' | '%') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    # TODO: Check types before the operation

    if operation == '*':
        return left * right
    
    if operation == '/':
        if right == 0:
            self.script_errors.showError(pos, "RUNTIME ERROR", "Math Error", "I don't do division by zero. Nobody does.")
            exit()
        return left // right

    if operation == '%':
        if right == 0:
            parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Math Error", "Modulo over zero? Bold of you to assume I'd allow that.")
            exit()
        return left % right
