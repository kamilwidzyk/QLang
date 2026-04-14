from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # ifStmt: IF '(' expr ')' block (ELSE block)?;

    # expr > 0 -> if block
    # expr == 0 -> else block

    expr = self.handle_block(block.expr(), block)
    if_block = None
    else_block = None

    if expr > 0: # Enter if block
        if_block = self.handle_block(block.block(0), block)
    elif block.block(1): # Enter else block if it's defined
        else_block = self.handle_block(block.block(1), block)

    # Nothing to run is condition is not satisfied and there is no else
    if if_block is None and else_block is None:
        return

    self.scopes.push(pos, scope_type="if")
    try:
        if if_block:
            for item in if_block:
                self.handle_block(item, parent=if_block)
        elif else_block:
            for item in else_block:
                self.handle_block(item, parent=else_block)
    finally:
        self.scopes.pop()