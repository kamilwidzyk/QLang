from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import * 
from .function_call import FunctionReturn

if TYPE_CHECKING:
    from place import Place

def handle_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    if "children" not in block:
        print("statementContext 'children' key missing")
        exit()

    children = block["children"]
    if len(children) == 0:
        return None

    # return stmt: RETURN expr? ';'
    if self.is_terminal(children[0], text='return', parent=block):
        return_val = None
        if len(children) > 1 and not self.is_terminal(children[1], text=';', parent=block):
            return_val = self.handle_block(children[1], parent=block)
        raise FunctionReturn(return_val)

    # execute any other statement normally and ignore return values from children
    for child in children:
        if self.is_terminal(child, text=';', parent=block):
            continue
        self.handle_block(child, parent=block)

    return None
