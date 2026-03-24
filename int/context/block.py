from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_block_ctx(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # 1. Terminal '{' (first child)
    # 2. Block of code to return (everything in between)
    # 3. Terminal '}' (last child)

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "BlockContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    if len(children) < 2:
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "BlockContext: at least 2 children required(empty block)")
        exit()

    if not self.is_terminal(children[0], text="{", parent=block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "BlockContext: child index 0, expected '{'")
        exit()

    if not self.is_terminal(children[-1], text="}", parent=block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "BlockContext: last child, expected '}'")
        exit()

    return children[1:-1]