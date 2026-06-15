from typing import Any, TYPE_CHECKING

from ....script_errors import ScriptErrors
from ....consts import *
from ...expression.variable_expression import handle_variable_expression, is_variable_expression
from ....exception.assignment_to_expression import AssignmentToExpressionException

from ....operations.operators import do_operation_or
from ....operations.variables import do_variable_assignment

if TYPE_CHECKING:
    from place import Place

from ....expression import Expression, TYPE_BOOL


def handle_or_eq_op(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '|=' expr
    # left is variable -> assign variable || right, return variable || right
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    right_value = self.handle_block(right_expr, block)

    if not is_variable_expression(left_expr):
        # code ATE-2
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr), code="2")

    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)

    bool_result = do_operation_or(left_variable.get(), right_value).value
    do_variable_assignment(self, left_variable, bool_result, pos)
    return Expression(TYPE_BOOL, bool_result)

    
    