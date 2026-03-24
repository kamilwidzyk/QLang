from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_and(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '&&' expr

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "AndExprContext: missing 'children' key or no children")
        exit()
    
    children = block["children"]

    if len(children) != 3:
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "AndExprContext: expected 3 children")
        exit()

    val1 = self.handle_block(children[0], parent=block)
    val2 = self.handle_block(children[2], parent=block)

    if not self.is_terminal(children[1], text='&&', parent=block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "AndExprContext: child index 1, expected '&&'")
        exit()
    
    return 1 if (val1 > 0) and (val2 > 0) else 0