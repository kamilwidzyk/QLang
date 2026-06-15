from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...variable import Variable
from ...exception.cant_find_variable import CantFindVariableException
from ...exception.spellcheck import get_spellcheck_suggestion
from ...exception.no_parent_scope import NoParentScopeException
from ...scope import Scope


if TYPE_CHECKING:
    from place import Place


def handle_operator_parent(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles parent operator
    ||| '^' ('^')* var
    Multiple '^' meaning:
    ^a -> parent::a
    ^^a -> parent::parent::a
    ^^^a -> parent::parent::parent::a
    """

    var_block = block.var()
    var_name = var_block.ID().getText()

    # count how many '^' (leading carets) are present
    text = block.getText()
    depth = 0
    for ch in text:
        if ch == '^':
            depth += 1
        else:
            break

    # resolve target scope by going `depth` levels up
    scope = self.scopes.current
    for _ in range(depth):
        if scope.parent is None:
            # code NPS-2
            raise NoParentScopeException(ScriptErrors.Position.extract(block), code="2")
        scope = scope.parent

    # check variable existence in that specific ancestor scope
    if var_name not in scope.vars:
        # code: CFV-6
        suggestion = get_spellcheck_suggestion(var_name, list(scope.vars.keys()))
        raise CantFindVariableException(ScriptErrors.Position.extract(var_block.ID()), var_name, code="6", suggestion=suggestion)

    variable = scope.vars[var_name]

    # handle indexing if present
    from ..variable.assigment import handle_index
    index_list = []
    for idx in var_block.index():
        index_list.append(handle_index(self, idx, var_block))

    # If it's a Variable instance, set its index for later access
    if isinstance(variable, Variable):
        variable.index = index_list

    return variable