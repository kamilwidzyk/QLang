from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_parentheses(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '(' expr ')'
    return self.handle_block([x for x in block.getChildren()][1], block)
