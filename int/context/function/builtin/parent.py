from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from place import Place

from ..common import _collect_call_args, _resolve_parent_value
from ....script_errors import ScriptErrors
from ....exception.kwargs_not_supported import KeywordArgumentsNotSupportedException

def builtin_parent(self: Place, block: Any):
    positional_args, keyword_args = _collect_call_args(self, block)
     
    # parent() doesn't support keyword args
    if keyword_args:
        block_pos = ScriptErrors.Position.extract(block)
        # code KANS-2
        raise KeywordArgumentsNotSupportedException(
            pos=block_pos,
            func_name="parent",
            code="2"
        )
    
    return _resolve_parent_value(self, block, positional_args, self.scopes.current)