from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_add_sub(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('+' | '-') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    result = None

    if operation == '+':
        result = left + right
    elif operation == '-':
        result = left - right

    # TODO: Negative values will be allowed only for num type
    if result < 0:
        result = 0

    return result