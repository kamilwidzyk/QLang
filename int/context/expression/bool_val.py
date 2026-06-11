from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_BOOL
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_bool(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    bool_value = block.getChild(0)
    if isinstance(bool_value, BoolValueTrueCtx):
        return Expression(TYPE_BOOL, True)
    if isinstance(bool_value, BoolValueFalseCtx):
        return Expression(TYPE_BOOL, False)
