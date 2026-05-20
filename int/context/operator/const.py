from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...context.variable.declaration import handle_const_variable_declaration, handle_const_existing_variable

if TYPE_CHECKING:
    from place import Place


def handle_operator_const(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # constDecl: CONST (varType constAssign (',' constAssign)* | ID);
    if block.varType() is not None:
        return handle_const_variable_declaration(self, block, parent, pos)
    return handle_const_existing_variable(self, block, parent, pos)
