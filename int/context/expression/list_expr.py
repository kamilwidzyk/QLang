from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import Obs, ObsRegister

from ...expression import Expression, TYPE_LIST

if TYPE_CHECKING:
    from place import Place

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
    
    return Expression(TYPE_LIST, lst, shape=len(lst))
    