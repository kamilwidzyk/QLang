from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_add_sub(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('+' | '-') expr 

    if not self.has_children(block):
        print("AddSubExprContext: missing 'children' key or no children")
        exit()
    
    children = block["children"]
    
    if len(children) != 3:
        print("AddSubExprContext: 3 children expected")
        exit()
    
    val1 = self.handle_block(children[0], parent=block)
    val2 = self.handle_block(children[2], parent=block)

    result = None

    if self.is_terminal(children[1], text='+', parent=block):
        result = val1 + val2
    elif self.is_terminal(children[1], text='-', parent=block):
        result = val1 - val2
    else:
        print("AddSubExprContext: child index 1, expected '+' or '-'")
        exit()

    if result < 0:
        result = 0

    return result