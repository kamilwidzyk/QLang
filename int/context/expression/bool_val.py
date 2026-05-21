from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place

def handle_bool(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # BOOL_VAL: 'T' | 'F';
    value = [x for x in block.getChildren()][0].getText()

    if value == 'T':
        return Expression(TYPE_BOOL, True)
    if value == 'F':
        return Expression(TYPE_BOOL, False)