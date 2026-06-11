from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors

if TYPE_CHECKING:
    from place import Place

def handle_parentheses(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles (), just executes whatever is inside
    ||| '(' expr ')'
    """
    return self.handle_block([x for x in block.getChildren()][1], block)
