
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from place import Place

from int.context.function.common import _collect_call_args, _parse_num_cast_value
from int.exception.builtin_expects_value import BuiltinExpectsValueException
from int.exception.kwargs_not_supported import KeywordArgumentsNotSupportedException
from int.exception.too_much_args import TooMuchArgumentsException
from int.script_errors import ScriptErrors

def builtin_num(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block)
    block_pos = ScriptErrors.Position.extract(block)

    # num() doesn't support keyword args
    if keyword_args:
        # code KANS-1
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="num",
            code="1"
        )

    if len(positional_args) != 1:
        # code TMA-2
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name="num",
            taken_args=len(positional_args),
            expected_args=1,
            code="2"
        )

    cast_value = _parse_num_cast_value(positional_args[0])
    if cast_value is None:
        # code BEV-1
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="num",
            expects="a number or a numeric string",
            code="1"
        )

    return cast_value