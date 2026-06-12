from typing import Any, TYPE_CHECKING

from int.exception.builtin_expects_value import BuiltinExpectsValueException
from int.exception.too_much_args import TooMuchArgumentsException
from int.expression import TYPE_INT, Expression

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args, _parse_num_cast_value
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_show_console(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block)
     
    # show_console() doesn't support keyword args
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-8
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="show_console",
            code="8"
        )

    if len(positional_args) != 1:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-8
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name="show_console",
            taken_args=len(positional_args),
            expected_args=1,
            code="8"
        )

    enable_value = _parse_num_cast_value(positional_args[0])
    if enable_value is None:
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-6
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="show_console",
            expects="0 or 1",
            code="6"
        )

    if int(enable_value.value) not in [0, 1]:
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-6
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="show_console",
            expects="0 or 1",
            code="6"
        )

    if getattr(self, "console", None) is not None:
        if int(enable_value.value) == 1:
            self.console.show()
        else:
            self.console.hide()

    return Expression(TYPE_INT, int(enable_value.value))