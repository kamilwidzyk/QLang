from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place

from ..statement import BreakLoop, ContinueLoop

def handle_while(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # whileStmt: WHILE '(' expr ')' block;

    self.scopes.push(pos, scope_type="while")
    try:
        while True:
            cond = self.handle_block(block.expr(), block)

            if isinstance(cond, Expression) and cond.type == TYPE_BOOL:
                cond_val = cond.value
            else:
                try:
                    cond_val = cond.value > 0
                except Exception:
                    cond_val = False

            if not cond_val:
                break

            try:
                for child in self.handle_block(block.block(), parent=block):
                    self.handle_block(child, parent=block)
            except ContinueLoop:
                continue
            except BreakLoop:
                break

    finally:
        self.scopes.pop()
