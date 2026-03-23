from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('*' | '/' | '%') expr 

    if not self.has_children(block):
        print("MulDivModExprContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) != 3:
        print("MulDivModExprContext: 3 children expected")
        exit()
    
    val1 = self.handle_block(children[0], parent=block)
    val2 = self.handle_block(children[2], parent=block)

    if self.is_terminal(children[1], text='*', parent=block):
        return val1 * val2
    elif self.is_terminal(children[1], text='/', parent=block):
        if val2 == 0:
            print("MulDivModExprContext: divide by zero")
            exit()
        return val1 // val2
    elif self.is_terminal(children[1], text='%', parent=block):
        if val2 == 0:
            print("MulDivModExprContext: mod over zero")
            exit()
        return val1 % val2
    else:
        print("MulDivModExprContext: child index 1, expected '*', '/' or '%'")
        exit()