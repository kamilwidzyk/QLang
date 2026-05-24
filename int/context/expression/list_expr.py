from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_LIST

if TYPE_CHECKING:
    from place import Place

def _expression_shape(value: Any):
    if isinstance(value, Expression) and value.type == TYPE_LIST:
        if isinstance(value.shape, list):
            return value.shape
        if isinstance(value.shape, int):
            return [value.shape]
    return []

def _list_shape(values: list):
    if not values:
        return [0]

    first_shape = _expression_shape(values[0])
    for value in values[1:]:
        if _expression_shape(value) != first_shape:
            return None

    return [len(values)] + first_shape

def handle_expression_list_empty(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    return Expression(TYPE_LIST, [], shape=[0])


def handle_expression_list_non_empty(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    lst = []
    for x in block.expr():
        result = self.handle_block(x, block)
        lst.append(result if isinstance(result, Expression) else Expression(TYPE_LIST, result) if isinstance(result, list) else result)
    return Expression(TYPE_LIST, lst, shape=_list_shape(lst))


def handle_expression_list_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    for x in block.getChildren():
        result = self.handle_block(x, block)
        return result

def handle_expression_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    lst = []
    exprs = block.expr() if hasattr(block, 'expr') else []
    if exprs is None:
        exprs = []

    for x in exprs:
        result = self.handle_block(x, block)
        lst.append(result if isinstance(result, Expression) else Expression(TYPE_LIST, result) if isinstance(result, list) else result)

    return Expression(TYPE_LIST, lst, shape=_list_shape(lst))
    
