from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place


def handle_while_loop(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # whileStmt: WHILE '(' expr ')' block;
    self.scopes.push(pos, scope_type="while")
    try:
        while self.handle_block(block.expr(), block) > 0:
            while_block = self.handle_block(block.block(), block)
            if while_block:
                for child in while_block:
                    self.handle_block(child, parent=block)
    finally:
        self.scopes.pop()
