from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from .variable_expression import handle_variable_expression
from ..QLang.QLangParser import QLangParser
from .pre_post import is_variable

if TYPE_CHECKING:
    from place import Place




def handle_mul_eq_op(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '*=' expr
    # left is variable -> assign variable * right, return variable * right
    # left is not variable -> return left * right, no assignment
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    left_variable = None
    left_value = None
    right_value = self.handle_block(right_expr, block)

    if is_variable(left_expr):
        left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)
        
    if left_variable is not None:
        var_name = left_variable.name
        var_value = left_variable.get()
        new_value = var_value * right_value
        left_variable.set(new_value)
        self.scopes.set(var_name, left_variable)
        return new_value
    
    left_value = self.handle_block(left_expr, block)
    return left_value * right_value
    