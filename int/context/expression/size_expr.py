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

    if isinstance(var, list):
        return Expression(TYPE_INT, len(var))
    elif isinstance(var, str):
        return Expression(TYPE_INT, len(var))
    elif hasattr(var, 'data') and isinstance(var.data, list):
        return Expression(TYPE_INT, len(var.data))
    elif var.dimensions == []:
        return Expression(TYPE_INT, 1)
    elif var.dimensions == [0]:
        return Expression(TYPE_INT, 1)
    else:
        return Expression(TYPE_INT, value=var.dimensions[0])

def handle_expression_size_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # # ID
    expr_result = self.handle_block(block.sizeGetter(), block)
    if isinstance(expr_result, Expression):
        return expr_result
    if isinstance(expr_result, list):
        return Expression(TYPE_INT, len(expr_result))
    elif isinstance(expr_result, str):
        return Expression(TYPE_INT, len(expr_result))
    elif hasattr(expr_result, 'dimensions'):
        return Expression(TYPE_INT, expr_result.dimensions[0] if expr_result.dimensions else 1)
    else:
        return Expression(TYPE_INT, 1)
