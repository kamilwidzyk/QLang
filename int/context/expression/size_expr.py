from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

from ...exception.cant_find_variable import CantFindVariableException
from ...variable import TYPE_LIST, TYPE_ARRAY
from ...expression import Expression, TYPE_INT

if TYPE_CHECKING:
    from place import Place

def handle_expression_size_getter(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # sizeGetter: '#' ID;   
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), var_name)
    
    var = self.scopes.get(var_name)

    if var.dimensions == [0] or var.dimensions == []:
        return 1

    return Expression(TYPE_INT, value=var.dimensions[0])

def handle_expression_size_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    return self.handle_block(block.sizeGetter(), block)