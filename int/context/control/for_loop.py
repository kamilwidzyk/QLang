from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...num import Num

from ...expression import Expression, TYPE_INT
from ..statement import BreakLoop, ContinueLoop
from ...operations.compare import do_compare_greater, do_compare_less

if TYPE_CHECKING:
    from place import Place



def handle_for_loop(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    For loop handler.

    ||| forStmt: FOR ID FROM expr TO expr (STEP expr)? block;
    
    for <ID> from <expr> to <expr> <block>
    for <ID> from <expr> to <expr> step <expr> <block>

    If step is not specified, it defaults to 1 if end value is greater than start value, otherwise -1.
    <ID> loop variable can be changed inside the loop, <expr> are re-evaluated each iteration

    'from' is inclusive, 'to' is exclusive

    """

    expressions = [x for x in block.expr()]
    var_name = block.ID().getText()    

    def parse_expr(start_expr, end_expr, step_expr=None) -> tuple:
        """
        Parses start, end and step expressions and returns their values as a tuple.
        """
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

    # Counter variable of type num with name <ID>
    counter = Num()
    counter.name = var_name

    # Enter new scope and add counter variable to it
    self.scopes.push(pos, scope_type="for")
    self.scopes.create(var_name, counter)

    # Parse expression before starting
    start_val, end_val, step_val = parse_expr(*expressions)

    # Set the counter to start value
    counter.set(start_val.extract_value())
    self.scopes.set(var_name, counter)

    try:
        # Repeat block until condition is met:
        # (start > end && counter > end) || (start < end && counter < end)
        while (do_compare_greater(start_val, end_val) and do_compare_greater(counter.get(), end_val)) or \
              (do_compare_less(start_val, end_val) and do_compare_less(counter.get(), end_val)):
            # Push new scope for this iteration to clear variables from previous iteration
            self.scopes.push(pos, scope_type="for_iteration")
            
            # Run code inside
            try:
                try:
                    self.execute_block(block.block(), parent=block)
                except ContinueLoop:
                    # continue to next iteration of loop body
                    break
            except BreakLoop:
                # break out of the while loop entirely
                self.scopes.pop()
                break
            finally:
                # Pop iteration scope to clear variables for next iteration
                self.scopes.pop()

            # parse expressions each time
            start_val, end_val, step_val = parse_expr(*expressions)

            # Increment counter by step value
            self.scopes.modify(var_name, lambda x: x + step_val)
    finally:
        # Exit scope
        self.scopes.pop()