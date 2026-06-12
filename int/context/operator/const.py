from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...context.variable.declaration import handle_const_variable_declaration, handle_const_existing_variable

if TYPE_CHECKING:
    from place import Place


def handle_operator_const(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles const operator
    ||| CONST (varType constAssign (',' constAssign)* | ID);
    If varType is present, it means we are declaring a new const variable
    If varType is not present, it means we are referencing an existing const variable
    Operation is performed using handle_const_variable_declaration or handle_const_existing_variable
    """
    if block.varType() is not None:
        return handle_const_variable_declaration(self, block, parent, pos)
    return handle_const_existing_variable(self, block, parent, pos)
