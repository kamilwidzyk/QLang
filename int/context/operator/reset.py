from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression
from ...variable import Variable

from ...exception.cant_find_variable import CantFindVariableException
from ...exception.spellcheck import get_spellcheck_suggestion
from ...exception.direct_quantum_access import DirectQuantumAccessException
from ...variable import TYPE_STATE
from ..variable.assigment import handle_index

if TYPE_CHECKING:
    from place import Place


def handle_var(self: "Place", block: Any, parent: Any) -> Variable:
    """
    Handle variable access with optional indexing applied to it
    """
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        # code: CFV-8
        suggestion = get_spellcheck_suggestion(var_name, self.scopes.get_all_names())
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), var_name, code="8", suggestion=suggestion)

    index_list = []
    for index in block.index():
        next_index = handle_index(self, index, block)
        index_list.append(next_index)

    var = self.scopes.get(var_name)
    var.index = index_list

    return var


def handle_reset_expr(self: "Place", block: Any, parent: Any, pos: ScriptErrors.Position) -> Expression:
    """
    Handles reset operator
    ||| reset: 'reset' var;
    """
    var = handle_var(self, block.var(), block)

    if var.type == TYPE_STATE:
        # code: DQA-4
        raise DirectQuantumAccessException(
            pos=ScriptErrors.Position.extract(block.var()), 
            code="4"
        )

    result = var.reset(ScriptErrors.Position.extract(block))
    self.scopes.set(var.name, var)
    return result
