from typing import Any, TYPE_CHECKING

from int.exception.index_not_int import IndexNotIntException

from ...script_errors import ScriptErrors
from ...consts import *

from ...exception.cant_find_variable import CantFindVariableException
from ...exception.direct_quantum_access import DirectQuantumAccessException
from ...index_types import SimpleIndex, RangeIndex, ListIndex
from ...expression import TYPE_BOOL, TYPE_FLOAT, TYPE_INT, TYPE_NUM, TYPE_OBS, Expression, TYPE_STATE, ValueResolver
from ...variable import Variable

if TYPE_CHECKING:
    from place import Place

def _coerce_index_value(value):
    value = ValueResolver.extract_raw_value(value)

    if isinstance(value, list):
        return [_coerce_index_value(item) for item in value]

    if isinstance(value, (int, bool)):
        return int(value)

    return value


def handle_index(self: Place, block: Any, parent: Any):
    """
    Parse an index context and return a SimpleIndex, RangeIndex, or ListIndex.
    
    Grammar:
        index
            : '[' expr DOTDOT expr ']'         -> RangeIndex
            | '[' '[' expr (',' expr)* ']' ']' -> ListIndex
            | '[' expr ']'                     -> SimpleIndex
            ;

    All indexes need to be int, if they are not IndexNotIntException is raised
    """
    # Detect which alternative was matched
    if block.DOTDOT() is not None:
        # Range index: [expr..expr]
        start_expr = self.handle_block(block.expr(0), block)
        end_expr = self.handle_block(block.expr(1), block)

        if(start_expr.type not in [TYPE_FLOAT, TYPE_INT, TYPE_BOOL, TYPE_NUM, TYPE_OBS]):
            # code INI-2
            raise IndexNotIntException(
                ScriptErrors.Position.extract(block.expr(0)),
                code="2"
            )
        if(end_expr.type not in [TYPE_FLOAT, TYPE_INT, TYPE_BOOL, TYPE_NUM, TYPE_OBS]):
            # code INI-3
            raise IndexNotIntException(
                ScriptErrors.Position.extract(block.expr(1)),
                code="3"
            )

        start_val = start_expr.get_value() if hasattr(start_expr, 'get_value') else start_expr.value
        end_val = end_expr.get_value() if hasattr(end_expr, 'get_value') else end_expr.value

        if(float(start_val) != int(start_val)): # start index is not int
            # code INI-2
            raise IndexNotIntException(
                ScriptErrors.Position.extract(block.expr(0)),
                code="2"
            )
        if(float(end_val) != int(end_val)): # end index is not int
            print("End value is not int:", end_val)
            # code INI-3
            raise IndexNotIntException(
                ScriptErrors.Position.extract(block.expr(1)),
                code="3"
            )

        return RangeIndex(int(start_val), int(end_val))
    
    # Check for list index: [[expr, expr, ...]]
    # List index has 2 LBRACK tokens
    lbrack_tokens = block.LBRACK()
    if lbrack_tokens is not None and len(lbrack_tokens) >= 2:
        # List index: [[a, b, c]]
        indices = []
        for expr in block.expr():
            val = self.handle_block(expr, block)
            index_values = _coerce_index_value(val)
            if isinstance(index_values, list):
                indices.extend(index_values)
            else:
                indices.append(index_values)

        for i in indices:
            if(float(i) != int(i)): # one of the indicies is not int
                # code INI-4
                raise IndexNotIntException(
                    ScriptErrors.Position.extract(block),
                    code="4"
                )
        return ListIndex(indices)

    # Simple index: [expr]
    index = self.handle_block(block.expr(0), block)
    index_value = _coerce_index_value(index)

    if isinstance(index_value, list):
        for i in index_value:
            if(float(i) != int(i)): # one of the indicies is not int
                # code INI-4
                raise IndexNotIntException(
                    ScriptErrors.Position.extract(block),
                    code="4"
                )
        return ListIndex(index_value)
    

    if(float(index_value) != int(index_value)):
        # code INI-5
        raise IndexNotIntException(
            ScriptErrors.Position.extract(block),
            code="5"
        )

    return SimpleIndex(index_value)

def handle_var(self: Place, block: Any, parent: Any) -> Variable:
    # var: ID index*; 

    var_name = block.ID().getText()

    if not self.scopes.exists(var_name):
        raise CantFindVariableException(ScriptErrors.Position.extract(block.ID()), var_name)

    index_list = []
    for index in block.index():
        index_list.append(
            handle_index(self, index, block)
        )
    
    var = self.scopes.get(var_name)
    var.index = index_list

    return var


def handle_assigment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles variable assignment
    ||| assignStmt: var '=' expr;
    """
    var = handle_var(self, block.var(), block)

    if var.type == TYPE_STATE:
        # code DQA-5
        raise DirectQuantumAccessException(pos=pos, code="5")

    assign_val = ValueResolver.resolve_for_operation(self.handle_block(block.expr(), block))
    var.set(assign_val, pos=pos)
    
    self.scopes.set(var.name, var)
