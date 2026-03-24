from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..function import Function
from ..scope import Scope

class FunctionReturn(Exception):
    """Control flow exception raised when a function returns a value."""
    def __init__(self, value: Any):
        super().__init__("Function return")
        self.value = value

if TYPE_CHECKING:
    from place import Place

def handle_function_call(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):

    # functionCallStmt: ID '(' argList? ')';

    # 1. Terminal <function_name> 
    # 2. Terminal '('
    # If has arguments:
    #   3. argList block
    # 4. Terminal ')'

    if not self.has_children(block):
        print("FunctionCallStmtContext")
        exit()
    
    children = block["children"]

    func_name = None
    args = []
    has_args = False

    for child_index in range(len(children)):
        child = children[child_index]
        if child_index == 0:
            func_name = self.extract_text(child, block)
        elif child_index == 1:
            if not self.is_terminal(child, text='(', parent=block):
                print("FunctionCallStmtContext: child index 1, expected '('")
                exit()
        elif child_index == 2:
            if self.is_type(child, type=ARG_LIST_CONTEXT, parent=block):
                args = self.handle_block(child, parent=block)
                has_args = True
            elif not self.is_terminal(child, text=')', parent=block):
                print("FunctionCallStmtContext: child index 2, expected ')'")
                exit()
        elif child_index == 3:
            if not has_args:
                print("FunctionCallStmtContext: child index 3, unexpected block")
                exit()
            if not self.is_terminal(child, text=")", parent=block):
                print("FunctionCallStmtContext: child index 3, expected ')'")
                exit()

    print("Function call: name: " + str(func_name) + " args: " + str(args))

    
    if not self.scopes.exists(func_name):
        print("FunctionCallStmtContext: Function does not exist")
        exit()

    # Call the function
    function_def: Function = self.scopes.get(func_name)

    # Create new scope for function
    new_scope = Scope(
        pos=pos,
        parent=function_def.closure_scope
    )

    # Add names functions args to it
    if function_def.params is not None:
        param_names = [p.name for p in function_def.params]
        for param_name, param_value in zip(param_names, args):
            new_scope.vars[param_name] = param_value
    
    # Switch execution context
    old_scope = self.scopes.current
    self.scopes.current = new_scope
    self.scopes.set(func_name, function_def)
    

    return_val = None
    # Execute function
    try:
        for func_block in function_def.body:
            self.handle_block(func_block)
    except FunctionReturn as ret:
        return_val = ret.value

    # Recover scope
    self.scopes.current = old_scope

    print("Function execution done")
    print("Return val: " + str(return_val))

    return return_val