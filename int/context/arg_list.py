from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_arg_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # argList: expr (',' expr)*;

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ArgListContext: missing 'children' key or no children")
        exit()
    
    children = block["children"]

    args = []

    expect_block = True

    for child in children:
        if expect_block:
            val = self.handle_block(child, block)
            args.append(val)
            expect_block = False
        else:
            if not self.is_terminal(child, text=',', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ArgListContext: expected ','")
                exit()
            expect_block = True

    return args