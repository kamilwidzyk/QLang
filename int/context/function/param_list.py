from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_param_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):  
    # paramList: param? (',' param)* multipleParam?;
    param_list = []

    for param in block.param():
        param_list.append(self.handle_block(param, block))

    # Handle multipleParam (*args)
    if hasattr(block, 'multipleParam') and block.multipleParam():
        multiple_param = block.multipleParam()
        param_name = multiple_param.ID().getText()
        # Create a special param for *args
        from ...function import FunctionParam
        varargs_param = FunctionParam(name=param_name, type="varargs", size=[], initial=None)
        param_list.append(varargs_param)

    return param_list