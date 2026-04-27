from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_param_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):  
    # paramList: param (',' param)*;
    param_list = []

    for param in block.param():
        param_list.append(self.handle_block(param, block))

    return param_list