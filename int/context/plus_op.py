from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_plus(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '+' expr
    val = self.handle_block(block.expr(), block)

    return val