from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...function import Function
from ...scope import Scope

class FunctionReturn(Exception):
    """Control flow exception raised when a function returns a value."""
    def __init__(self, value: Any):
        super().__init__("Function return")
        self.value = value

if TYPE_CHECKING:
    from place import Place

def handle_function_call(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # functionCallStmt: ID '(' argList? ')';

    # TODO: Add support for multiple arguments and names arguments

    func_name = block.ID().getText()
    args = None
    if block.argList():
        args = self.handle_block(block.argList(), block)
    
    block_pos = ScriptErrors.Position.extract(block) 
    
    # Check if the function exists
    if not self.scopes.exists(func_name):
        self.script_errors.showError(
            pos=block_pos, 
            error_type="RUNTIME ERROR", 
            title="ExecutionError", 
            msg="Tried calling that function: No one picked up.")
        exit()

    # Get the function
    function_def: Function = self.scopes.get(func_name)

    # Check if it's a function(variable call is possible but not legal)
    if not function_def.type == "Function":
        self.script_errors.showError(
            pos=block_pos, 
            error_type="RUNTIME ERROR", 
            title="ExecutionError", 
            msg=f"I tried to call '{func_name}' but a variable picked up.")
        exit()

    # Check if call has the same number of arguments
    # No arguments in definition and some in call:
    if function_def.params is None and args is not None:
        self.script_errors.showError(
            pos=block_pos, 
            error_type="RUNTIME ERROR", 
            title="ExecutionError", 
            msg=f"'{func_name}' does not take arguments.")
        exit()
    # arguments count does not match
    if function_def.params is not None:
        if len(function_def.params) != len(args):
            self.script_errors.showError(
                pos=block_pos, 
                error_type="RUNTIME ERROR", 
                title="ExecutionError", 
                msg=f"'{func_name}' takes exaclty {len(function_def.params)} arguments. {len(args)} given.")
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