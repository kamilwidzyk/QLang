from typing import Any, TYPE_CHECKING

import math

from int.exception.builtin_expects_value import BuiltinExpectsValueException
from int.exception.too_much_args import TooMuchArgumentsException
from int.expression import TYPE_FLOAT, TYPE_INT, Expression

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_cut_round_floor_ceil(self: Place, block: Any, func_name: str):
    positional_args, keyword_args = _collect_call_args(self, block, func_name)
     
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-9
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name=func_name,
            code="9"
        )

    if len(positional_args) == 0 or len(positional_args) > 2:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-9
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name=func_name,
            taken_args=len(positional_args),
            expected_args=2,
            code="9"
        )

    try:
        val_raw = positional_args[0].extract_raw_value()
        if not isinstance(val_raw, (int, float)):
            raise ValueError()
        val = float(val_raw)
    except (AttributeError, ValueError, TypeError):
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-7
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name=func_name,
            expects="a number",
            code="7"
        )

    if len(positional_args) == 2:
        try:
            decimals_raw = positional_args[1].extract_raw_value()
            if not isinstance(decimals_raw, (int, float)):
                raise ValueError()
            decimals = int(decimals_raw)
        except (AttributeError, ValueError, TypeError):
            block_pos = ScriptErrors.Position.extract(block)
            # code BEV-8
            raise BuiltinExpectsValueException(
                pos=block_pos,
                func_name=func_name,
                expects="a number for decimal places",
                code="8"
            )
    else:
        decimals = 0

    factor = 10.0 ** decimals
    val_scaled = val * factor

    if func_name == "cut":
        res = math.trunc(val_scaled) / factor
    elif func_name == "round":
        if val_scaled > 0:
            res = math.floor(val_scaled + 0.5) / factor
        else:
            res = math.ceil(val_scaled - 0.5) / factor
    elif func_name == "floor":
        res = math.floor(val_scaled) / factor
    elif func_name == "ceil":
        res = math.ceil(val_scaled) / factor

    if decimals <= 0:
        return Expression(TYPE_INT, int(res))
    else:
        return Expression(TYPE_FLOAT, float(res))