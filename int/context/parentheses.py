from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_parentheses(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '(' expr ')'

    if not self.has_children(block):
        print("ParenExprContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) != 3:
        print("ParenExprContext: 3 children expected")
        exit()

    if not self.is_terminal(children[0], text='(', parent=block):
        print("ParenExprContext: child index 0, expected '('")
        exit()
    
    if not self.is_terminal(children[2], text=')', parent=block):
        print("ParentExprContext: child index 2, expected ')'")
        exit()
    
    return self.handle_block(children[1], parent=block)