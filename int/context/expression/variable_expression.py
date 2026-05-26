from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import ParenExprCtx, VarExprCtx, ParentExprCtx
from ...expression import Expression, TYPE_NUM, TYPE_STATE
from ...num import Num
from ...variable import Variable
from ...QLang.QLangParser import QLangParser

from ...exception.cant_find_variable import CantFindVariableException
from ...exception.direct_quantum_access import DirectQuantumAccessException
from ..operator.parent import handle_operator_parent
from ..variable.assigment import handle_index

if TYPE_CHECKING:
    from place import Place


def is_variable_expression(block: Any) -> bool:
    if isinstance(block, VarExprCtx):
        return True
    if isinstance(block, ParentExprCtx):
        return True
    if isinstance(block, ParenExprCtx):
        inner = block.expr()
        return inner is not None and is_variable_expression(inner)
    return False


def handle_variable_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position, return_variable=False):
    # ID ('[' expr ']')* or ^...var or parenthesized variable expressions
    if isinstance(block, ParentExprCtx):
        variable = handle_operator_parent(self, block, parent, pos)

        if return_variable:
            return variable

        if isinstance(variable, Expression):
            return variable

        if isinstance(variable, Variable):
            if variable.type == TYPE_STATE:
                # code: DQA-1
                raise DirectQuantumAccessException(
                    pos=pos,
                    code="1"
                )   
            if variable.type == TYPE_NUM:
                return variable.get_value()
            return variable.get()

        return variable

    if isinstance(block, ParenExprCtx):
        return handle_variable_expression(self, block.expr(), block, pos, return_variable)

    # ID ('[' expr ']')*
    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        # code: CFV-3
        raise CantFindVariableException(
            pos=ScriptErrors.Position.extract(block.ID()), 
            var_name=var_name,
            code="3"
        )

    variable = self.scopes.get(var_name)

    index = []
    
    for idx_ctx in block.index():
        index.append(
            handle_index(self, idx_ctx, block)
        )

    # For lists (like varargs), handle indexing directly
    if isinstance(variable, list):
        if index:
            from ...index_types import SimpleIndex
            result = variable
            for idx in index:
                if isinstance(idx, SimpleIndex):
                    idx = idx.resolve(len(result))
                result = result[int(idx) if not isinstance(idx, int) else idx]
            return Expression("value", result) if not isinstance(result, Expression) else result
        return variable

    variable.index = index

    if return_variable:
        return variable

    if isinstance(variable, Expression):
        return variable

    if isinstance(variable, Variable):
        if variable.type == TYPE_STATE:
            # code: DQA-2
            raise DirectQuantumAccessException(
                pos=pos,
                code="2"
            )
        if variable.type == TYPE_NUM:
            return variable.get_value()
        return variable.get()

    if isinstance(variable, Num):
        return variable.get()

    if variable is int:
        return variable

    if isinstance(variable, Expression):
        return variable

    return variable

