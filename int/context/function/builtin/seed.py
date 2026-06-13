from typing import Any, TYPE_CHECKING

from int.exception.builtin_expects_value import BuiltinExpectsValueException
from int.exception.too_much_args import TooMuchArgumentsException

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args, _get_seed_expression, _set_seed
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_seed(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block, "seed")
     
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-4
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="seed",
            code="4"
        )

    if len(positional_args) == 0:
        return _get_seed_expression()

    if len(positional_args) != 1:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-4
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name="seed",
            taken_args=len(positional_args),
            expected_args=1,
            code="4"
        )

    seed_value = _set_seed(positional_args[0])
    if seed_value is None:
        block_pos = ScriptErrors.Position.extract(block)
        # code BEV-3
        raise BuiltinExpectsValueException(
            pos=block_pos,
            func_name="seed",
            expects="a number",
            code="3"
        )

    if getattr(self, "quantum_client", None) is not None:
        self.quantum_client.seed(seed_value.value)

    return seed_value