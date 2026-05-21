from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place

from ...exception.cant_find_variable import CantFindVariableException

def _value_of(item):
    return item.value if isinstance(item, Expression) else item

def handle_reference(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # reference: '@' ID;

    ID = block.ID().getText()

    if not self.scopes.exists(ID):
        # code: CFV-7
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), ID, code="7")

    variable = self.scopes.get(ID)

    return variable    
