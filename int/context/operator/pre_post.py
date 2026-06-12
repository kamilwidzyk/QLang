from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ..expression.variable_expression import handle_variable_expression, is_variable_expression
from ...QLang.QLangParser import QLangParser

from ...exception.assignment_to_expression import AssignmentToExpressionException

from ...operations.variables import do_variable_pre_decrement
from ...operations.variables import do_variable_post_decrement
from ...operations.variables import do_variable_pre_increment
from ...operations.variables import do_variable_post_increment

if TYPE_CHECKING:
    from place import Place

def is_variable(var: Any) -> bool:
    return is_variable_expression(var)


def handle_pre_decrement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles pre-decrement operation
    ||| '--' expr
    Calculation is performed using do_variable_pre_decrement
    """
    expression = block.expr()

    if not is_variable(expression):
        # code: ATE-9
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression), code="9")

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_pre_decrement(self, variable)


def handle_post_decrement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles post-decrement operation
    ||| expr '--'
    Calculation is performed using do_variable_post_decrement
    """
    expression = block.expr()

    if not is_variable(expression):
        # code: ATE-10
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression), code="10")

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_post_decrement(self, variable)
    

def handle_pre_increment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles pre-increment operation
    ||| '++' expr
    Calculation is performed using do_variable_pre_increment
    """
    expression = block.expr()

    if not is_variable(expression):
        # code: ATE-11
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression), code="11")

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_pre_increment(self, variable)
    

def handle_post_increment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles post-increment operation
    ||| expr '++'
    Calculation is performed using do_variable_post_increment
    """
    expression = block.expr()

    if not is_variable(expression):
        # code: ATE-12
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression), code="12")

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_post_increment(self, variable)

    