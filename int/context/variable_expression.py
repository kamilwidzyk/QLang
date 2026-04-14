from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_variable_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # ID ('[' expr ']')? 

    var_name = block.ID().getText()
    index = None
    if block.expr():
        index = self.handle_block(block.expr(), block)

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    # Check if variable exists
    if not self.scopes.exists(var_name):
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="ExistenceError", 
            msg=f"I can't find '{var_name}' in this universe, does it even exist?")
        exit()

    # Get the variable
    variable = self.scopes.get(var_name)

    if type(variable) == int:
        return variable

    # Check if it can be read
    if variable.type in ["StateRegister", "State"]:
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="Access Denied", 
            msg="You can't access a quantum state like that. Try measuring it first.")
        exit()

    if index is not None:
        # Check if variable supports index
        if variable.type != "ObsRegister":
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="Access denied", 
                msg="There is nothing more, just a 0 or 1.")
            exit()

        # Check if index is int
        if int(index) != index:
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="QuantizationError", 
                msg="Try looking at the bits, not between them.")
            exit()
            
        # Check if index is >= 0
        if index < 0:
            self.script_errors.showError(
                pos=parent_pos, 
                error_type="RUNTIME ERROR", 
                title="BoundaryBreach", 
                msg=f"You attempted to access index {index}. Aren't you scared of going into the unknown.")
            exit()
        
        # Return the value as 0/1 (not bool)
        return 1 if variable[index] else 0
    
    
    if variable.type == "Obs":
        return 1 if variable.get() else 0
    
    if variable.type == "ObsRegister":
        return variable.get() 
    
    self.script_errors.showError(
        pos=parent_pos, 
        error_type="RUNTIME ERROR", 
        title="Type Error", 
        msg=f"What is this variable of type '{variable.type}' doing here?")
    exit()