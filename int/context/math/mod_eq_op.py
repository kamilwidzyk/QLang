from typing import Any, TYPE_CHECKING

from int.exception.modulo_over_zero import ModuloOverZeroException

from ...script_errors import ScriptErrors
from ...consts import *
from ..expression.variable_expression import handle_variable_expression, is_variable_expression 
from .mul_div_mod import is_text_or_string

from ...exception.assignment_to_expression import AssignmentToExpressionException

from ...operations.operators import do_operation_mod


if TYPE_CHECKING:
    from place import Place


def handle_mod_eq_op(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles compound modulus operation
    ||| expr '%=' expr
    Calculation is performed using do_operation_mod
    """
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    if not is_variable_expression(left_expr):
        # code: ATE-5
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr), code="5")

    right_value = self.handle_block(right_expr, block)
    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)
        
    var_name = left_variable.name
    var_value = left_variable.get()

    if not is_text_or_string(var_value) and right_value == 0:
        # code MOZ-2
        raise ModuloOverZeroException(ScriptErrors.Position.extract(right_expr), code="2")

    new_value = do_operation_mod(var_value, right_value).value
    left_variable.set(new_value)
    self.scopes.set(var_name, left_variable)
    return new_value
    
    