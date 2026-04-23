from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from .variable_expression import handle_variable_expression
from ..QLang.QLangParser import QLangParser

from ..exception.assignment_to_expression import AssignmentToExpressionException

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

    var_name = variable.name
    var_value = variable.get()
    var_value -= 1
    variable.set(var_value)
    self.scopes.set(var_name, variable)
    return var_value

def handle_post_decrement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '--'
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    var_name = variable.name
    orig_value = variable.get()
    variable.set(orig_value - 1)
    self.scopes.set(var_name, variable)
    return orig_value

def handle_pre_increment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # '++' expr
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))

    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    var_name = variable.name
    var_value = variable.get()
    var_value += 1
    variable.set(var_value)
    self.scopes.set(var_name, variable)
    return var_value

def handle_post_increment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr '++'
    expression = block.expr()

    if not is_variable(expression):
        raise AssignmentToExpressionException(ScriptErrors.Position.extract(expression))
    
    variable = handle_variable_expression(self, expression, block, pos, return_variable=True)

    var_name = variable.name
    orig_value = variable.get()
    variable.set(orig_value + 1)
    self.scopes.set(var_name, variable)
    return orig_value