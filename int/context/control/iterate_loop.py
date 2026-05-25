from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...num import Num
from ...expression import Expression, TYPE_INT, TYPE_FLOAT, TYPE_LIST, TYPE_NUM, TYPE_TEXT, TYPE_OBS

from ..statement import BreakLoop, ContinueLoop

if TYPE_CHECKING:
    from place import Place

def handle_iterate(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # iterateStmt: ITERATE expr AS ID (INDEX ID)? block;
    
    list_expr = block.expr()
    list_val = self.handle_block(list_expr, block)
    ids = block.ID()
    var_name = ids[0].getText()
    index_var_name = None
    if len(ids) > 1:
        index_var_name = ids[1].getText()
    
    elements = []
    
    if isinstance(list_val, Expression):
        if isinstance(list_val.value, (list, tuple)):
            elements = list(list_val.value)
        else:
            elements = [list_val]
    elif isinstance(list_val, list):
        elements = list_val
    else:
        elements = [list_val]
    
    self.scopes.push(pos, scope_type="iterate")
    placeholder_var = Expression(TYPE_INT, 0)  
    placeholder_var.name = var_name
    self.scopes.create(var_name, placeholder_var)
    
    if index_var_name:
        index_var = Num()
        index_var.name = index_var_name
        self.scopes.create(index_var_name, index_var)
    
    iterate_block = self.handle_block(block.block())
    
    try:
        for idx, element in enumerate(elements):
            self.scopes.push(pos, scope_type="iterate_iteration")
            
            try:
                element_var = self.scopes.get(var_name)
                
                if isinstance(element, Expression):
                    element_var.value = element.value
                    element_var.type = element.type
                    element_var.variable = getattr(element, 'variable', None)
                elif isinstance(element, Num):
                    expr = element.get()
                    element_var.value = expr.value
                    element_var.type = expr.type
                    element_var.variable = getattr(expr, 'variable', None)
                elif hasattr(element, 'get_value'):
                    raw_value = element.get_value()
                    if isinstance(raw_value, int):
                        element_var.type = TYPE_INT
                        element_var.value = raw_value
                    elif isinstance(raw_value, float):
                        element_var.type = TYPE_FLOAT
                        element_var.value = raw_value
                    elif isinstance(raw_value, str):
                        element_var.type = TYPE_TEXT
                        element_var.value = raw_value
                    elif isinstance(raw_value, list):
                        element_var.type = TYPE_LIST
                        element_var.value = raw_value
                    else:
                        element_var.type = TYPE_TEXT
                        element_var.value = str(raw_value)
                elif isinstance(element, list):
                    element_var.type = TYPE_LIST
                    element_var.value = element
                else:
                    if isinstance(element, int):
                        element_var.type = TYPE_INT
                        element_var.value = element
                    elif isinstance(element, float):
                        element_var.type = TYPE_FLOAT
                        element_var.value = element
                    else:
                        element_var.type = TYPE_TEXT
                        element_var.value = str(element)
                
                self.scopes.set(var_name, element_var)
                
                if index_var_name:
                    index_var = self.scopes.get(index_var_name)
                    index_var.set(idx)
                    self.scopes.set(index_var_name, index_var)
                
                try:
                    for child in iterate_block:
                        try:
                            self.handle_block(child, parent=block)
                        except ContinueLoop:
                            break
                except BreakLoop:
                    self.scopes.pop()
                    break
            finally:
                self.scopes.pop()
    
    finally:
        self.scopes.pop()


