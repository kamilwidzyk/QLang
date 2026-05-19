from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ..expression.variable_expression import handle_variable_expression, is_variable_expression
from ...QLang.QLangParser import QLangParser

from ...exception.assignment_to_expression import AssignmentToExpressionException
from ...operations.operators import do_operation_add

if TYPE_CHECKING:
    from place import Place

def handle_plus_eq_op(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '+=' expr
    # left is variable -> assign variable + right, return variable + right
    # left is not variable -> return left + right, no assignment
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    if not is_variable_expression(left_expr):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr))

    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)
    right_value = self.handle_block(right_expr, block)
        
    var_name = left_variable.name
    var_value = left_variable.get()
    new_value = do_operation_add(var_value, right_value)
    left_variable.set(new_value)
    self.scopes.set(var_name, left_variable)
    return new_value
    
    