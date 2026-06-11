from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_LIST

if TYPE_CHECKING:
    from place import Place

def _expression_shape(value: Any):
    """
    Returns first dimension shape of given expression
    !!! Shape needs to be stored inside the expression
    """
    if isinstance(value, Expression) and value.type == TYPE_LIST:
        if isinstance(value.shape, list):
            return value.shape
        if isinstance(value.shape, int):
            return [value.shape]
    return []

def _list_shape(values: list) -> list:
    """
    Returns a list of list shapes [first, second, ...]
    """
    if not values:
        return [0]

    next_shape = _expression_shape(values[0])
    for value in values[1:]:
        if _expression_shape(value) != next_shape:
            return None

    return [len(values)] + next_shape


###### NOT USED ########
def handle_expression_list_empty(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles empty list []
    """
    return Expression(TYPE_LIST, [], shape=[0])

###### NOT USED ########
def handle_expression_list_non_empty(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    lst = []
    for x in block.expr():
        result = self.handle_block(x, block)
        lst.append(result if isinstance(result, Expression) else Expression(TYPE_LIST, result) if isinstance(result, list) else result)
    return Expression(TYPE_LIST, lst, shape=_list_shape(lst))


def handle_expression_list_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handler to unwrap the list 
    """
    for x in block.getChildren():
        result = self.handle_block(x, block)
        return result

def handle_expression_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handle list expression
    """
    lst = []
    exprs = block.expr() if hasattr(block, 'expr') else []
    if exprs is None:
        exprs = []

    for x in exprs:
        result = self.handle_block(x, block)
        lst.append(result if isinstance(result, Expression) else Expression(TYPE_LIST, result) if isinstance(result, list) else result)

    return Expression(TYPE_LIST, lst, shape=_list_shape(lst))
    
