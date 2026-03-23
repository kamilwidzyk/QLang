from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_bool(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # BOOL_VAL: 'T' | 'F';

    if not self.has_children(block):
        print("BoolExprContext: missing 'children' key or no children")
        exit()

    if self.is_terminal(block["children"][0], text='T', parent=block):
        return 1
    elif self.is_terminal(block["children"][0], text='F', parent=block):
        return 0
    else:
        print("BoolExprContext: child index 0, expected 'T' or 'F'")
        exit()