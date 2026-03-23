from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_power(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '**' expr

    if not self.has_children(block):
        print("PowExprContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) != 3:
        print("PowExprContext: 3 children required")
        exit()

    if not self.is_terminal(children[1], text="**", parent=block):
        print("PowExprContext: second child needs to be '**'")
        exit()
    
    base = self.handle_block(children[0], parent=block)
    power = self.handle_block(children[2], parent=block)

    result = base ** power
    return result
