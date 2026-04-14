from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_arg_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # argList: expr (',' expr)*;
    
    return [self.handle_block(expr, block) for expr in block.expr()]
