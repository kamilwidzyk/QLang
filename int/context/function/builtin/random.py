from typing import Any, TYPE_CHECKING
import random

from int.exception.too_much_args import TooMuchArgumentsException
from int.expression import TYPE_FLOAT, Expression

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_random(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block, "random")
     
    # random() doesn't support keyword args
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-5
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="random",
            code="5"
        )

    # random() expects no positional args
    if len(positional_args) != 0:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-5
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name="random",
            taken_args=len(positional_args),
            expected_args=0,
            code="5"
        )

    # Return a float expression in range [0, 1)
    return Expression(TYPE_FLOAT, random.random())