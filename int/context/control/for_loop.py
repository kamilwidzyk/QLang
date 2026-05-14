from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...obs import ObsRegister
from ...num import Num

from ...expression import Expression, TYPE_INT
from ..statement import BreakLoop, ContinueLoop
from ...operations.compare import do_compare_greater, do_compare_greater_equal, do_compare_less, do_compare_less_equal
from ...operations.operators import do_operation_add

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
            if do_compare_greater(end_val, start_val).get_value():
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
        while (do_compare_greater(start_val, end_val) and do_compare_greater(counter.get(), end_val)) or \
              (do_compare_less(start_val, end_val) and do_compare_less(counter.get(), end_val)):
            # Run code inside
            try:
                for child in for_block:
                    try:
                        self.handle_block(child, parent=block)
                    except ContinueLoop:
                        # continue to next iteration of loop body
                        break
            except BreakLoop:
                # break out of the while loop entirely
                break

            start_val, end_val, step_val = parse_expr(*expressions)


            # Get the current value of the counter(it might got chenged inside the loop)
            counter = self.scopes.get(var_name)
            current_val = do_operation_add(counter.get(), step_val)
            counter.set(current_val)
            self.scopes.set(var_name, counter)

    finally:
        # Exit scope
        self.scopes.pop()

    #print("For loop: done")