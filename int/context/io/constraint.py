from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_constraint(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # OPTION A: expr '..' expr    -> 3 child
    # OPTION B: 'range' '(' expr ',' expr ')'  -> 6 child

    return self.handle_block(block.expr(0), block), \
            self.handle_block(block.expr(1), block)
