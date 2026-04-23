from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from .variable_expression import handle_variable_expression
from ..QLang.QLangParser import QLangParser

from ..exception.assignment_to_expression import AssignmentToExpressionException

from ..operations.variables import do_variable_pre_decrement
from ..operations.variables import do_variable_post_decrement
from ..operations.variables import do_variable_pre_increment
from ..operations.variables import do_variable_post_increment

if TYPE_CHECKING:
    from place import Place

def is_variable(var: Any) -> bool:
    return isinstance(var, QLangParser.VarExprContext) 


def handle_pre_decrement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '--' expr
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_pre_decrement(self, variable)


def handle_post_decrement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '--'
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_post_decrement(self, variable)
    

def handle_pre_increment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '++' expr
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_pre_increment(self, variable)
    

def handle_post_increment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '++'
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))
    
    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    return do_variable_post_increment(self, variable)

    