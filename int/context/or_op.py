from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_or(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '||' expr
    children = [x for x in block.expr()]
    left = self.handle_block(children[0], block)
    right = self.handle_block(children[1], block)

    return 1 if (left > 0) or (right > 0) else 0