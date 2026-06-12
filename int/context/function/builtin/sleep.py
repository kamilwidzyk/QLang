from typing import Any, TYPE_CHECKING

import time

from int.exception.builtin_expects_value import BuiltinExpectsValueException
from int.exception.too_much_args import TooMuchArgumentsException

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args, _resolve_parent_value
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_sleep(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block)
     
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-10
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="sleep",
            code="10"
        )

    if len(positional_args) != 1:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-10
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name="sleep",
            taken_args=len(positional_args),
            expected_args=1,
            code="10"
        )

    try:
        val_raw = positional_args[0].extract_raw_value()
        if not isinstance(val_raw, (int, float)):
            raise ValueError()
        sleep_time = float(val_raw)
    except (AttributeError, ValueError, TypeError):
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-9
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="sleep",
            expects="a number (seconds)",
            code="9"
        )

    time.sleep(sleep_time)