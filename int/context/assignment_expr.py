from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from .variable_expression import handle_variable_expression
from .pre_post import is_variable


if TYPE_CHECKING:
    from place import Place


def handle_assignment_expr(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '=' expr
    # 5 = 10, return is 10(ignore the 5)
    # VarExpr = 10, return is 10 and VarExpr is set to 10
    left_expr = block.expr(0)
    right_expr = block.expr(1)

    left_variable = None

    if is_variable(left_expr):
        left_variable = handle_variable_expression(self, left_expr, block, pos, return_variable=True)

    right_value = self.handle_block(right_expr, block)

    if left_variable is not None:
        var_name = left_variable.name
        left_variable.set(right_value)
        self.scopes.set(var_name, left_variable)
    
    return right_value