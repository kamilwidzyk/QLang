from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

from ...exception.cant_find_variable import CantFindVariableException
from ...variable import TYPE_LIST, TYPE_ARRAY, Variable
from ...expression import Expression, TYPE_INT, TYPE_ARRAY, TYPE_BOOL, TYPE_FLOAT, TYPE_TEXT, TYPE_OBS, TYPE_OBS_REGISTER, TYPE_NUM, TYPE_STRING

if TYPE_CHECKING:
    from place import Place

def handle_expression_size_getter(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # sizeGetter: '#' ID;   
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), var_name)

    # there might be something calculated wrong
    var = self.scopes.get(var_name)

    if isinstance(var, list):
        return Expression(TYPE_INT, len(var))
    elif isinstance(var, str):
        return Expression(TYPE_INT, len(var))
    elif hasattr(var, 'data') and isinstance(var.data, list):
        return Expression(TYPE_INT, len(var.data))
    elif isinstance(var, Variable):
        if var.type in [TYPE_LIST, TYPE_ARRAY]:
            return Expression(TYPE_INT, var.dimensions[0])
        if var.type == TYPE_TEXT:
            return Expression(TYPE_INT, len(var.data.get()))
        if var.type in [TYPE_OBS, TYPE_OBS_REGISTER, TYPE_NUM]:
            return Expression(TYPE_INT, 1 if var.dimensions == [0] else var.dimensions[0])
    elif isinstance(var, Expression):
        if var.type in [TYPE_LIST, TYPE_ARRAY]:
            return Expression(TYPE_INT, var.dimensions[0])
        if var.type == TYPE_STRING:
            return Expression(TYPE_INT, len(var.value))
        if var.type == TYPE_TEXT:
            return Expression(TYPE_INT, len(var.value.get()))
        if var.type in [TYPE_OBS, TYPE_OBS_REGISTER, TYPE_NUM]:
            return Expression(TYPE_INT, 1 if var.dimensions == [0] else var.dimensions[0])

    return Expression(TYPE_INT, 1)

def handle_expression_size_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '#' ID
    return self.handle_block(block.sizeGetter(), block)
    
