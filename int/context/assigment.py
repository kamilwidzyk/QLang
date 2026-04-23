from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

from ..exception.cant_find_variable import CantFindVariableException
from ..exception.information_leak import InformationLeakException

if TYPE_CHECKING:
    from place import Place

def handle_assigment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # assignStmt: ID ('[' expr ']')? '=' expr;
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        raise CantFindVariableException(var_name)

    variable = self.scopes.get(var_name)

    expr_node = block.expr()[-1] if isinstance(block.expr(), list) else block.expr()
    new_value = self.handle_block(expr_node, block)

    # check if it's an array assignment
    is_array_assign = '[' in [child.getText() for child in block.getChildren()]

    try:
        if is_array_assign:
            index = self.handle_block(block.expr()[0], block)
            new_value = self.handle_block(block.expr()[1], block)

            variable.set(index, new_value)
        else:
            new_value = self.handle_block(block.expr(), block) if not isinstance(block.expr(), list) else self.handle_block(block.expr()[0], block)
            variable.set(new_value)

    except OverflowError:
        raise InformationLeakException(
            pos=ScriptErrors.Position.extract(block),
            var_name=var_name,
            new_value=new_value,
            bits=variable.size
        )
    except IndexError:
        self.script_errors.showError(
            pos=pos,
            error_type="RUNTIME ERROR",
            title="Index Out Of Bounds",
            msg=f"You're trying to reach an index in '{var_name}' that doesn't exist in this dimension."
        )
        exit()
    except TypeError as e:
        self.script_errors.showError(
            pos=pos,
            error_type="RUNTIME ERROR",
            title="Type Error",
            msg=f"Cannot perform indexed assignment on '{var_name}': {str(e)}"
        )
        exit()

    self.scopes.set(var_name, variable)