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
    print("list empty")
    raise NotImplementedError()

def handle_expression_list_non_empty(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    print("list non empty")
    raise NotImplementedError()


def handle_expression_list_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    print("list expr: " + block.getText())
    for x in block.getChildren():
        result = self.handle_block(x, block)
        print("Result: " + str(result))
        return result

def handle_expression_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    print("list: " + block.getText())
    lst = []

    for x in block.expr():
        print("List element text: " + x.getText())
        
        result = self.handle_block(x, block)
        print("List element result: " + str(result) + str(result.get()))
        lst.append(result)
        print(lst)
        # return self.handle_block(x, block)
    print(lst)
    
    return Expression(TYPE_LIST, lst, shape=_list_shape(lst))
    
