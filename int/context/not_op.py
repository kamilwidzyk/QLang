from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_not(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '!' expr

    if not self.has_children(block):
        print("NotExprContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) != 2:
        print("NotExprContext: 2 children expected")
        exit()

    if not self.is_terminal(children[0], text='!', parent=block):
        print("NotExprContext: child index 0, expected '!'")
        exit()

    val = self.handle_block(children[1], parent=block)

    return 1 if val == 0 else 0