from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_obs_definition(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # obsDef: ID ('[' expr ']')?;

    # 1. Terminal <variable_name> (must be valid name)
    # If size specified:
    #   2a. Terminal '['
    #   2b. expr -> handle to get size
    #   2c. Terminal ']'

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDefContext: missing 'children' key or no children")
        exit()

    children = block["children"]

    var_name = None
    var_size = None
    size_specified = False

    for child_index in range(len(children)):
        child = children[child_index]

        if child_index == 0:
            var_name = self.extract_text(child, parent=block)
            if not self.is_valid_name(var_name):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDefContext: variable name is not valid")
                exit()
        elif child_index == 1:
            if not self.is_terminal(child, text='[', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDefContext: child index 1, expected '['")
                exit()
            size_specified = True
        elif child_index == 2:
            if not size_specified:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDefContext: child index 2, unexpected block")
                exit()
            var_size = self.handle_block(child, parent=block)
        elif child_index == 3:
            if not size_specified:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDefContext: child index 3, unexpected block")
                exit()
            if not self.is_terminal(child, text=']', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ObsDefContext: child index 3, expected ']'")
                exit()
    
    if self.scopes.exists(var_name):
        parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
        self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Name Error", "ObsDefContext: variable name already exists")
        exit()

    if var_size <= 0:
        parent_pos = ScriptErrors.Position.extract(parent) if parent else pos
        self.script_errors.showError(parent_pos, "RUNTIME ERROR", "Value Error", "ObsDefContext: variable size is <= 0")
        exit()

    variable = None

    if size_specified:
        variable = ObsRegister(var_size)
    else:
        variable = Obs()

    self.scopes.create(var_name, variable)