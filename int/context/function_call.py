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

    func_name = block.ID().getText()
    args = None
    if block.argList():
        args = self.handle_block(block.argList(), block)
    
    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
    
    # Check if the function exists
    if not self.scopes.exists(func_name):
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="You Error", 
            msg="Tried calling that function: No one picked up.")
        exit()

    # Get the function
    function_def: Function = self.scopes.get(func_name)

    # Check if it's a function(variable can is possible but not legal)
    if not function_def.type == "Function":
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="ExecutionError", 
            msg=f"I tried to call '{func_name}' but a variable picked up.")
        exit()

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

    return return_val