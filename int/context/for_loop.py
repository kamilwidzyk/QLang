from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_for_loop(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # TODO: start, end and step are now int only, this will change after adding num
    # forStmt: FOR ID FROM expr TO expr (STEP expr)? block;
    expressions = [x for x in block.expr()]
    var_name = block.ID().getText()
    start_val = int(self.handle_block(expressions[0], block))
    end_val = int(self.handle_block(expressions[1], block))

    step_val = None
    if len(expressions) == 3:
        step_val = int(self.handle_block(expressions[2], block))
    
    for_block = self.handle_block(block.block())

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    # Start, end and step values
    if start_val < 0:
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="Value Error", 
            msg="Start < 0. I only count from 0 and up.")
        exit()

    if end_val < 0:
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="Value Error", 
            msg="End value < 0? That loop ends before is begins.")
        exit()
    
    # Default step value
    if step_val is None:
        step_val = 1

    if step_val < 0:
        self.script_errors.showError(
            pos=parent_pos, 
            error_type="RUNTIME ERROR", 
            title="Value Error", 
            msg="Negative step? I'm not walking backwards through this loop.")
        exit()

    if end_val < start_val:
        return # do not run loop
    
    # make current_val counter
    current_val = ObsRegister(32)
    current_val.set(start_val)

    # Enter new scope
    self.scopes.push(pos, scope_type="for")
    self.scopes.create(var_name, current_val)

    try:
        # Repeat block until current_val <= end_val
        while current_val.get() <= end_val:
            for child in for_block:
                self.handle_block(child, parent=block)

            current_val.set(current_val.get() + step_val)
            self.scopes.set(var_name, current_val)
    finally:
        # Exit scope
        self.scopes.pop()

    #print("For loop: done")