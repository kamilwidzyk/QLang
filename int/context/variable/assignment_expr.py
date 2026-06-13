from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ..expression.variable_expression import handle_variable_expression
from ..operator.pre_post import is_variable
from ...expression import TYPE_STATE

from ...exception.assignment_to_expression import AssignmentToExpressionException
from ...exception.direct_quantum_access import DirectQuantumAccessException


if TYPE_CHECKING:
    from place import Place


def handle_assignment_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles variable assignment
    ||| expr '=' expr
    This variable is an expression -> assigned value is returned
    """
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    if not is_variable(left_expr):
        # code: ATE-13
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr), code="13")

    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)
    if left_variable.type == TYPE_STATE:
        # code DQA-6
        raise DirectQuantumAccessException(pos=pos, code="6")
    
    right_value = self.handle_block(right_expr, block)
        
    var_name = left_variable.name
    left_variable.set(right_value, pos=pos)
    self.scopes.set(var_name, left_variable)
    

    return right_value
