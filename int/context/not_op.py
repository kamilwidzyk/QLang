from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_not(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '!' expr
    val = self.handle_block(block.expr(), block)

    return 1 if val == 0 else 0