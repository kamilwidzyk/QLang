from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors

if TYPE_CHECKING:
    from place import Place

from ..statement import BreakLoop

from .if_condition import check_condition

def handle_while(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles while loop.
    ||| whileStmt: WHILE '(' expr ')' block;

    while (<condition>) <block>

    <condition> can be:
        - bool -> check if true
        - else -> check if > 0

    continue and break statements are supported inside the loop
        
    """
    # 

    while True:
        # break loop if condition is not satisfied
        cond = self.handle_block(block.expr(), block)
        if not check_condition(cond, pos):
            break
        
        # Enter new scope
        self.scopes.push(pos, scope_type="while")
        break_requested = False
        try:
            try:
                # execute code
                self.execute_block(block.block(), block)
            except BreakLoop:
                break_requested = True
        finally:
            self.scopes.pop()

        if break_requested:
            break
