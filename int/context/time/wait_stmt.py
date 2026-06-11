from typing import Any, TYPE_CHECKING
import time

from ...script_errors import ScriptErrors
from ...expression import TYPE_INT, TYPE_NUM, TYPE_FLOAT

from ...exception.wait_duration_not_numeric import WaitDurationNotNumericException




if TYPE_CHECKING:
    from ...place import Place

def handle_wait_stmt(self: 'Place', block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles the wait statement.

    ||| waitStmt: WAIT '(' expr timeUnit ')' ;

    wait(<duration> <unit>);
    <duration> can be any numeric expression (int, num, float)
    <unit> can be:
        - sec, second, seconds 
        - ms, millis, millisecond, milliseconds
        - min, minute, minutes
        - hour, hours

    """
    wait_block = block
    
    expr_val = self.handle_block(wait_block.expr(), wait_block)
    if expr_val.type not in [TYPE_INT, TYPE_NUM, TYPE_FLOAT]:
        # code: WDNN-1
        raise WaitDurationNotNumericException(
            pos=ScriptErrors.Position.extract(wait_block.expr()),
            received_type=expr_val.type,
            code="1"
        )
    
    duration = expr_val.extract_value()

    unit = self.handle_block(wait_block.timeUnit(), wait_block)
    multiplier = unit.get_second_multiplier()
    wait_time = duration * multiplier
    
    if wait_time > 0:
        time.sleep(wait_time)
    # TODO: Negative time error???
