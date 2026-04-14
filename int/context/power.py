from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_power(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '**' expr
    children = [x for x in block.expr()]
    base = self.handle_block(children[0], block)
    power = self.handle_block(children[1], block)

    return base ** power