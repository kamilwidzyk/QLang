from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...num import Num
from ...expression import Expression, TYPE_BOOL, TYPE_INT, TYPE_FLOAT, TYPE_LIST, TYPE_TEXT

from ..statement import BreakLoop, ContinueLoop

if TYPE_CHECKING:
    from place import Place


def _resolve_iterable(value: Any) -> list:
    """
    Resolves the given value to an iterable.
    """
    if isinstance(value, Expression):
        value = value.get_value()
    elif hasattr(value, 'get_value'):
        value = value.get_value()
    elif hasattr(value, 'get'):
        value = value.get()

    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _expression_from_element(element: Any, dimensions: list = None) -> Expression:
    """
    Convert any element to an expression, trying to preserve its type if possible.
    """
    if isinstance(element, Expression):
        return element

    raw = Expression._to_primitive(element)
    if isinstance(raw, Expression):
        return raw

    if isinstance(raw, tuple):
        raw = list(raw)

    if isinstance(raw, list):
        expr = Expression(TYPE_LIST, raw, shape=[len(raw)])
        expr.dimensions = expr.shape
        return expr
    if isinstance(raw, bool):
        return Expression(TYPE_BOOL, raw)
    if isinstance(raw, int):
        return Expression(TYPE_INT, raw)
    if isinstance(raw, float):
        return Expression(TYPE_FLOAT, raw)
    if isinstance(raw, str):
        return Expression(TYPE_TEXT, raw)

    return Expression(TYPE_TEXT, str(raw))


def handle_iterate(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles iterate loop.

    ||| iterateStmt: ITERATE expr AS ID (INDEX ID)? block;

    iterate <list> as <ID> <block>
    iterate <list> as <ID> index <indexID> <block>

    <list> can be written in place, be a variable or any expression that evaluates to a list.
    index starts from 0 and goes up by 1 each iteration

    if <list> is not a list, it will be treated as a single element list [<list>]

    continue/break supported

    """
    # Extract variable names
    ids = [id.getText() for id in block.ID()]
    var_name = ids[0]
    index_var_name = ids[1] if len(ids) > 1 else None

    # Get the elements to iterate over
    elements = _resolve_iterable(self.handle_block(block.expr(), block))

    # Start a new scope and create the iteration variable
    self.scopes.push(pos, scope_type="iterate")
    placeholder_var = Expression(TYPE_INT, 0)
    placeholder_var.name = var_name
    self.scopes.create(var_name, placeholder_var)
    
    # Create index variable if specified
    if index_var_name: 
        index_var = Num()
        index_var.name = index_var_name
        self.scopes.create(index_var_name, index_var)
    
    try:
        for idx, element in enumerate(elements): # iterate over the list
            self.scopes.push(pos, scope_type="iterate_iteration")
            
            try:
                # set the iteration variable to the current element
                element_var = _expression_from_element(element, elements.dimensions if isinstance(elements, Expression) and elements.type == TYPE_LIST else None)
                element_var.name = var_name
                self.scopes.set(var_name, element_var)
                
                # set index variable if specified
                if index_var_name:
                    self.scopes.modify(index_var_name, lambda _: idx)
                
                # execute the loop block
                try:
                    self.execute_block(block.block(), block)
                except BreakLoop:
                    break
            finally:
                self.scopes.pop()
    
    finally:
        self.scopes.pop()


