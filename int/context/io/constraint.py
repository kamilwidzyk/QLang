from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_constraint(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles constraints in two formats for now(range will be removed)
    ||| expr '..' expr
    ||| 'range' '(' expr ',' expr ')'
    """

    return self.handle_block(block.expr(0), block), \
            self.handle_block(block.expr(1), block)
