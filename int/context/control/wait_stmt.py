from typing import Any, TYPE_CHECKING
import time

from ...script_errors import ScriptErrors
from ...expression import TYPE_INT, TYPE_NUM, TYPE_FLOAT

from ...exception.unknown_time_unit import UnknownTimeUnitException
from ...exception.wait_duration_not_numeric import WaitDurationNotNumericException

if TYPE_CHECKING:
    from ...place import Place

def handle_wait_stmt(self: 'Place', block: Any, parent: Any, pos: ScriptErrors.Position):
    wait_block = block
    
    expr_val = self.handle_block(wait_block.expr(), wait_block)
    if expr_val.type not in [TYPE_INT, TYPE_NUM, TYPE_FLOAT]:
        ex = WaitDurationNotNumericException(
            pos=ScriptErrors.Position.extract(wait_block.expr()),
            received_type=expr_val.type,
            code="1"
        )
        ex.code_str = wait_block.expr().getText()
        raise ex
        
    val = expr_val.value
    while hasattr(val, 'get_value'):
        val = val.get_value()
    duration = float(val)
    
    unit = wait_block.ID().getText().lower()
    
    multiplier = 1.0
    if unit in ['s', 'sec', 'second', 'seconds']:
        multiplier = 1.0
    elif unit in ['ms', 'millisecond', 'milliseconds']:
        multiplier = 0.001
    elif unit in ['m', 'min', 'minute', 'minutes']:
        multiplier = 60.0
    elif unit in ['h', 'hour', 'hours']:
        multiplier = 3600.0
    else:
        raise UnknownTimeUnitException(
            pos=ScriptErrors.Position.extract(wait_block.ID()),
            unit=unit,
            code="1"
        )
        
    wait_time = duration * multiplier
    
    if wait_time > 0:
        time.sleep(wait_time)
