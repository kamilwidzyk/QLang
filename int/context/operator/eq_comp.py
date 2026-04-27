from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_eq_comp(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('==' | '!=') expr
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    right = self.handle_block(children[2], block)

    if children[1].getText() == "==":
        return 1 if left == right else 0
    else:
        return 1 if left != right else 0
    