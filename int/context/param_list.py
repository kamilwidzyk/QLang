from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_param_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):   
    param_list = []

    if not self.has_children(block):
        print("ParamListContext: 'children' key missing or no children")
        exit()

    children = block["children"] 

    for child_index in range(len(children)):
        child = children[child_index]
        # ignore Terminals ','
        if not self.is_terminal(child, text=',', parent=block):
            param_list.append(self.handle_block(child, block))

    return param_list