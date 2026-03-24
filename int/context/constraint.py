from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_constraint(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # OPTION A: expr '..' expr    -> 3 child
    # OPTION B: 'range' '(' expr ',' expr ')'  -> 6 child

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "ConstraintContext: 'children' key missing or no children")
        exit()

    children = block["children"]

    if len(children) == 3:
        if not self.is_terminal(children[1], text='..', parent=block):
            self.script_errors.showError(pos, "SYNTAX ERROR", "Expected ':'", "ConstraintContext: Expected '..'")
            exit()
        return self.handle_block(children[0], parent=block), self.handle_block(children[2], parent=block)
    elif len(children) == 6:
        if not self.is_terminal(children[0], text='range', parent=block):
            self.script_errors.showError(pos, "SYNTAX ERROR", "Expected 'range'", "ConstraintContext: Expected 'range'")
            exit()
        if not self.is_terminal(children[1], text='(', parent=block):
            self.script_errors.showError(pos, "SYNTAX ERROR", "Expected '('", "ConstraintContext: Expected '('")
            exit()
        if not self.is_terminal(children[3], text=',', parent=block):
            self.script_errors.showError(pos, "SYNTAX ERROR", "Expected ','", "ConstraintContext: Expected ','")
            exit()
        if not self.is_terminal(children[5], text=')', parent=block):
            self.script_errors.showError(pos, "SYNTAX ERROR", "Expected ')'", "ConstraintContext: Expected ')'")
            exit()
        return self.handle_block(children[2], parent=block), self.handle_block(children[4], parent=block)
    else:
        self.script_errors.showError(pos, "SYNTAX ERROR", "Invalid syntax", "3 or 6 child expected")
        exit()
