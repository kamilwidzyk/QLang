from typing import Any, TYPE_CHECKING

from ....script_errors import ScriptErrors
from ....consts import *

from ....operations.operators import do_operation_or

if TYPE_CHECKING:
    from place import Place

def handle_or(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '||' expr
    children = [x for x in block.expr()]
    left = self.handle_block(children[0], block)
    right = self.handle_block(children[1], block)

    return do_operation_or(left, right)