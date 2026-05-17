from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ..expression.variable_expression import handle_variable_expression
from ..operator.pre_post import is_variable
from ...expression import TYPE_STATE

from ...exception.assignment_to_expression import AssignmentToExpressionException


if TYPE_CHECKING:
    from place import Place


def handle_assignment_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '=' expr
    # 5 = 10, return is 10(ignore the 5)
    # VarExpr = 10, return is 10 and VarExpr is set to 10
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    left_variable = None

    if not is_variable(left_expr):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr))

    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)
    if left_variable.type == TYPE_STATE:
        self.script_errors.showError(
            pos=pos,
            error_type="RUNTIME ERROR",
            title="Access Denied",
            msg="Quantum states cannot be assigned directly.",
        )
        exit()
    right_value = self.handle_block(right_expr, block)
        
    var_name = left_variable.name
    left_variable.set(right_value)
    self.scopes.set(var_name, left_variable)
    

    return right_value
