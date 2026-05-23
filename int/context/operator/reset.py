from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression
from ...variable import Variable

from ...exception.cant_find_variable import CantFindVariableException
from ...exception.index_not_int import IndexNotIntException
from ...exception.direct_quantum_access import DirectQuantumAccessException
from ...variable import TYPE_INT, TYPE_STATE
from ..variable.assigment import handle_index

if TYPE_CHECKING:
    from place import Place


def handle_var(self: "Place", block: Any, parent: Any) -> Variable:
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        # code: CFV-8
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), var_name, code="8")

    index_list = []
    for index in block.index():
        index_list.append(handle_index(self, index, block))

    var = self.scopes.get(var_name)
    var.index = index_list

    return var


def handle_reset_expr(self: "Place", block: Any, parent: Any, pos: ScriptErrors.Position) -> Expression:
    var = handle_var(self, block.var(), block)

    if var.type == TYPE_STATE:
        # code: DQA-4
        raise DirectQuantumAccessException(ScriptErrors.Position.extract(block), var.name, code="4")

    result = var.reset()
    self.scopes.set(var.name, var)
    return result
