from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_eq_comp(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('==' | '!=') expr

    if not self.has_children(block):
        print("EqExprContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) != 3:
        print("EqExprContext: 3 children expected")
        exit()

    val1 = self.handle_block(children[0], parent=block)
    val2 = self.handle_block(children[2], parent=block)

    if self.is_terminal(children[1], text='==', parent=block):
        return 1 if val1 == val2 else 0
    elif self.is_terminal(children[1], text='!=', parent=block):
        return 1 if val1 != val2 else 0
    else:
        print("EqExprContext: child index 1, expected '==' or '!='")
        exit()