from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ..expression.variable_expression import handle_variable_expression
from ...QLang.QLangParser import QLangParser
from ..operator.pre_post import is_variable

from ...exception.assignment_to_expression import AssignmentToExpressionException
from ...exception.divide_by_zero import DivideByZeroException

from ...operations.operators import do_operation_div, do_operation_div_int
from ...expression import TYPE_INT

if TYPE_CHECKING:
    from place import Place


def handle_div_eq_op(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '/=' expr
    # left is variable -> assign variable / right, return variable / right
    # left is not variable -> return left / right, no assignment
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    if not is_variable(left_expr):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr))

    right_value = self.handle_block(right_expr, block)

    if right_value == 0:
        raise DivideByZeroException(ScriptErrors.Position.extract(right_expr))

    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)
        
    var_name = left_variable.name
    var_value = left_variable.get()

    if var_value.type == TYPE_INT and right_value == TYPE_INT:
        new_value = do_operation_div_int(var_value, right_value)
    else:
        new_value = do_operation_div(var_value, right_value)
    left_variable.set(new_value)
    self.scopes.set(var_name, left_variable)
    return new_value
    
    