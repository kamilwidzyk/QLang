from typing import Any, TYPE_CHECKING

from int.exception.too_much_args import TooMuchArgumentsException

if TYPE_CHECKING:
    from place import Place

from ..common import _coerce_import_path, _collect_call_args, _import_source_functions, _resolve_parent_value
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_import_source(self: Place, block: Any, func_name: str):
    positional_args, keyword_args = _collect_call_args(self, block)
     
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-6
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name=func_name,
            code="6"
        )

    if len(positional_args) != 1:
        block_pos = ScriptErrors.Position.extract(block)
        # code TMA-6
        raise TooMuchArgumentsException(
            pos=block_pos,
            func_name=func_name,
            taken_args=len(positional_args),
            expected_args=1,
            code="6"
        )

    block_pos = ScriptErrors.Position.extract(block)
    file_path = _coerce_import_path(positional_args[0], func_name, block_pos)
    _import_source_functions(self, file_path, block_pos)
    return None