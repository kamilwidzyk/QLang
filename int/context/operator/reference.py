from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place

from ...exception.cant_find_variable import CantFindVariableException
from ...exception.spellcheck import get_spellcheck_suggestion

def handle_reference(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles variable reference
    ||| reference: '@' ID;
    Returns variable instead of its value
    """
    ID = block.ID().getText()

    if not self.scopes.exists(ID):
        # code: CFV-7
        suggestion = get_spellcheck_suggestion(ID, self.scopes.get_all_names())
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), ID, code="7", suggestion=suggestion)

    return self.scopes.get(ID)
