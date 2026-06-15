from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors

from ...exception.cant_find_variable import CantFindVariableException
from ...exception.spellcheck import get_spellcheck_suggestion
from ...variable import TYPE_LIST, TYPE_ARRAY, Variable
from ...expression import Expression, TYPE_INT, TYPE_ARRAY, TYPE_BOOL, TYPE_FLOAT, TYPE_TEXT, TYPE_OBS, TYPE_NUM, TYPE_STRING

if TYPE_CHECKING:
    from place import Place

def extract_variable_size(var: Any) -> int:
    """
    Returns size of a given variable/expression
    """
    if isinstance(var, (list, str)):
        return Expression(TYPE_INT, len(var))
    elif hasattr(var, 'data') and isinstance(var.data, list):
        return Expression(TYPE_INT, len(var.data))
    elif isinstance(var, Variable):
        try:
            if var.type in [TYPE_LIST, TYPE_ARRAY]:
                return Expression(TYPE_INT, var.dimensions[0])
            if var.type == TYPE_TEXT:
                return Expression(TYPE_INT, len(var.data.get()))
            if var.type in [TYPE_OBS, TYPE_NUM]:
                return Expression(TYPE_INT, 1 if var.dimensions == [0] else var.dimensions[0])
        except Exception:
            return Expression(TYPE_INT, 0)
    elif isinstance(var, Expression):
        try:
            if var.type in [TYPE_LIST, TYPE_ARRAY]:
                return Expression(TYPE_INT, var.dimensions[0])
            if var.type == TYPE_STRING:
                return Expression(TYPE_INT, len(var.value))
            if var.type == TYPE_TEXT:
                return Expression(TYPE_INT, len(var.value.get()))
            if var.type in [TYPE_OBS, TYPE_NUM]:
                return Expression(TYPE_INT, 1 if var.dimensions == [0] else var.dimensions[0])
        except Exception:
            return Expression(TYPE_INT, 0)

    return Expression(TYPE_INT, 1)

def handle_expression_size_getter(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles size operator
    ||| sizeGetter: '#' ID;   

    Depending of the type it returns:
        - list: shape of first dimension
        - text: length in characters
        - single value: 1
        - other: 0 or undefined behaviour

    """
    # 
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        # code: CFV-1
        suggestion = get_spellcheck_suggestion(var_name, self.scopes.get_all_names())
        raise CantFindVariableException(
            pos=ScriptErrors.Position.extract(block.ID()), 
            var_name=var_name,
            code="1",
            suggestion=suggestion
        )

    var = self.scopes.get(var_name)
    return extract_variable_size(var)

    

def handle_expression_size_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Unwrap the size getter operator, execution in expression_size_getter handler
    """
    return self.handle_block(block.sizeGetter(), block)
    
