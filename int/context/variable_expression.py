from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_variable_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # ID ('[' expr ']')? 

    # 1. Terminal <variable_name>
    # If index specified:
    #   2a. Terminal '['
    #   2b. expression block -> handle to get index
    #   2c. Terminal ']'

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "VarExprContext: 'children' key missing or not children")
        exit()

    children = block["children"]

    var_name = None
    index = None
    index_specified = False

    for child_index in range(len(children)):
        child = children[child_index]
        if child_index == 0:
            var_name = self.extract_text(child, parent=block)
        elif child_index == 1: 
            if not self.is_terminal(child, text="[", parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "VarExprContext: child index 1, expected '['")
                exit()
            index_specified = True
        elif child_index == 2:
            if not index_specified:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "VarExprContext: child index 2, unexpected block")
                exit()
            index = self.handle_block(child, block)
        elif child_index == 3:
            if not index_specified:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "VarExprContext: child index 3, unexpected block")
                exit()
            if not self.is_terminal(child, text="]", parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "VarExprContext: child index 3, expected ']'")
                exit()
        else:
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "VarExprContext: child index > 3, unexpected block")
            exit()
    
    #print("VarExprContext parsed")
    #print("Name: " + str(var_name))
    #print("Index: " + str(index))

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    if not self.scopes.exists(var_name):
        self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Name Error", "VarExprContext: variable '" + str(var_name) + "' does not exist")
        exit()

    variable = self.scopes.get(var_name)

    if type(variable) == int:
        return variable

    if variable.type in ["StateRegister", "State"]:
        self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Type Error", "VarExprContext: attempted reading of quantum state")
        exit()

    if index_specified:
        if int(index) != index or index < 0:
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Value Error", "VarExprContext: index is not int or < 0")
            exit()

        if variable.type != "ObsRegister":
            self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Type Error", "VarExprContext: attempted accesing index of non index obs")
            exit()
        
        return 1 if variable[index] else 0
    
    if variable.type == "Obs":
        return 1 if variable.get() else 0
    
    if variable.type == "ObsRegister":
        return variable.get() 
    
    self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Type Error", "varExprContext: incorrect variable type: " + variable.type)
    exit()