from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from .variable_expression import handle_variable_expression
from ..QLang.QLangParser import QLangParser
from .pre_post import is_variable

from ..exception.assignment_to_expression import AssignmentToExpressionException

from ..operations.operators import do_operation_and
from ..operations.variables import do_variable_assignment

if TYPE_CHECKING:
    from place import Place



def handle_and_eq_op(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '&=' expr
    # left is variable -> assign variable && right, return variable && right
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    right_value = self.handle_block(right_expr, block)

    if not is_variable(left_expr):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(left_expr))

    left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)

    new_value = do_operation_and(left_variable.get(), right_value)
    return do_variable_assignment(self, left_variable, new_value)

    
    