from typing import Any, TYPE_CHECKING

from int.exception.builtin_expects_value import BuiltinExpectsValueException
from int.exception.too_much_args import TooMuchArgumentsException
from int.expression import TYPE_INT, Expression

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args, _parse_num_cast_value
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_packet_log(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block, "packet_log")
     
    # packet_log() doesn't support keyword args
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-7
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="packet_log",
            code="7"
        )

    if len(positional_args) != 1:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-7
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name="packet_log",
            taken_args=len(positional_args),
            expected_args=1,
            code="7"
        )

    enable_value = _parse_num_cast_value(positional_args[0])
    if enable_value is None:
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-5
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="packet_log",
            expects="0 or 1",
            code="5"
        )

    if int(enable_value.value) not in [0, 1]:
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-5
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="packet_log",
            expects="0 or 1",
            code="5"
        )

    self.packet_log_enabled = bool(int(enable_value.value))
    return Expression(TYPE_INT, int(enable_value.value))