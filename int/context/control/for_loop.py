from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import ObsRegister
from ...num import Num

from ...expression import Expression, TYPE_INT

if TYPE_CHECKING:
    from place import Place

def handle_for_loop(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # forStmt: FOR ID FROM expr TO expr (STEP expr)? block;
    expressions = [x for x in block.expr()]
    var_name = block.ID().getText()
    

    def parse_expr(start_expr, end_expr, step_expr=None) -> tuple:
        start_val = self.handle_block(start_expr, block)    
        end_val = self.handle_block(end_expr, block)

        step_val = None
        if step_expr is not None:
            step_val = self.handle_block(step_expr, block)

        # Default step value
        if step_val is None:
            step_val = Expression(TYPE_INT)
            if end_val.value > start_val.value:
                step_val.value = 1
            else:
                step_val.value = -1

        return start_val, end_val, step_val

    # make counter
    counter = Num()
    counter.name = var_name

    # Enter new scope
    self.scopes.push(pos, scope_type="for")
    self.scopes.create(var_name, counter)

    # parse range and step
    start_val, end_val, step_val = parse_expr(*expressions)
    for_block = self.handle_block(block.block())

    parent_pos = ScriptErrors.Position.extract(parent) if parent else pos

    # set start value to counter
    counter.set(start_val.value)
    self.scopes.set(var_name, counter)

    try:
        # Repeat block until condition is met
        while (start_val.value > end_val.value and counter.get().value > end_val.value) or \
              (start_val.value < end_val.value and counter.get().value < end_val.value):
            # Run code inside
            for child in for_block:
                self.handle_block(child, parent=block)

            
            start_val, end_val, step_val = parse_expr(*expressions)


            # Get the current value of the counter(it might got chenged inside the loop)
            counter = self.scopes.get(var_name)
            current_val = counter.get().value
            current_val += step_val.value
            counter.set(current_val)
            self.scopes.set(var_name, counter)

    finally:
        # Exit scope
        self.scopes.pop()

    #print("For loop: done")