from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # ifStmt: IF '(' expr ')' block (ELSE block)?;

    # expr > 0 -> if block
    # expr == 0 -> else block

    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: missing 'children' key or no children")
        exit()

    # 1. Terminal 'if'
    # 2. Terminal '('
    # 3. condition -> handle to get value
    # 4. Terminal ')'
    # 5. BlockContext -> if block
    # Else defined:
    #   6a. Terminal 'else'
    #   6b. BlockContext -> else block

    if_block = None
    else_block = None
    else_defined = False
    condition = None

    children = block["children"]

    for child_index in range(len(children)):
        child = children[child_index]

        if child_index == 0: # Terminal 'if'
            if not self.is_terminal(child, text='if', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: child index 0, expected 'if'")
                exit()
        elif child_index == 1: # Terminal '('
            if not self.is_terminal(child, text='(', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: child index 1, expected '('")
                exit()
        elif child_index == 2: # condition
            condition = self.handle_block(child, parent=block)
        elif child_index == 3: # Terminal ')'
            if not self.is_terminal(child, text=')', parent=block):
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: child index 3, expected ')'")
                exit()
        elif child_index == 4: # if block
            if_block = self.handle_block(child, parent=block)
        elif child_index == 5: # Terminal 'else'
            if self.is_terminal(child, text='else', parent=block):
                else_defined = True
            else:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: child index 5, expected 'else'")
                exit()
        elif child_index == 6:
            if not else_defined:
                self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: child index 6, unexpected block")
                exit()
            else_block = self.handle_block(child, parent=block)
        else:
            self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "IfStmtContext: child index > 6, unexpected block")
            exit()

    condition_satisfied = condition > 0
    enter_scope = condition_satisfied or else_defined

    if not enter_scope:
        return
    
    #print("Entering new scope")

    self.scopes.push(pos, scope_type="if")
    try:
        if condition_satisfied:
            for item in if_block:
                self.handle_block(item, parent=if_block)
        elif else_defined:
            for item in else_block:
                self.handle_block(item, parent=else_block)
    finally:
        #print("Exiting scope")
        self.scopes.pop()