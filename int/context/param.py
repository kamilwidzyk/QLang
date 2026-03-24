from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..function import FunctionParam

if TYPE_CHECKING:
    from place import Place

def handle_param(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # param: (STATE | OBS) ID ('[' NUMBER ']')?;

    # 1. Terminal 'state' or 'obs' => param type
    # 2. Terminal <variable_name> => param name (must be a valid name)
    # If size specified:
    #   3a. Terminal '['
    #   3b. Number -> handle block to get value
    #   3c. Terminal ']'

    param_type = None
    param_name = None
    param_size = None
    size_specified = False

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: 'children' key missing or no children")
        exit()

    children = block["children"]

    for child_index in range(len(children)):
        child = children[child_index]

        if child_index == 0: # 1. Terminal 'state' or 'obs'
            if self.is_terminal(child, text="state", parent=block):
                param_type = "state"
            elif self.is_terminal(child, text="obs", parent=block):
                param_type = "obs"
            else:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index 0, expected terminal 'state' or 'obs'")
                exit()
        elif child_index == 1: # 2. Terminal <variable_name>
            param_name = self.extract_text(child, parent=block)
            if not self.is_valid_name(param_name):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index 1, param name is not valid")
                exit()
        elif child_index == 2: # 3a. Terminal '[' 
            if not self.is_terminal(child, text='[', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index 2, unexpected block")
                exit()
            size_specified = True
        elif child_index == 3: # 3b. Number
            if not size_specified:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index 3, unexpected block")
                exit()
            param_size = self.handle_block(child, parent=block)
        elif child_index == 4: # 3c. Terminal ']'
            if not size_specified:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index 4, unexpected block")
                exit()
            if not self.is_terminal(child, text="]", parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index 4, expected ']'")
                exit()
        else:
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ParamContext: child index > 4, unexpected block")
            exit()

    return FunctionParam(name=param_name, type=param_type, size=param_size)