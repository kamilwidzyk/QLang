from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...function import FunctionParam

if TYPE_CHECKING:
    from place import Place


def handle_param_varParamDefault(self: Place, block: Any, parent: Any, type: str):
    """
     Handles the parsing of a parameter with optional default value and size.
     ||| varParamDefault: ID ('[' INT_NUMBER ']')* ('=' expr)?;
    """
    param_name = block.ID().getText()
    param_size = []
    for size_num in block.INT_NUMBER():
        param_size.append(self.handle_block(size_num, block))
    param_default = None
    if block.expr():
        param_default = self.handle_block(block.expr(), block)

    return FunctionParam(name=param_name, type=type, size=param_size, initial=param_default)


def handle_param(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handling moved to handle_param_varParamDefault 
    """
    # param: varType varParamDefault;

    varType = block.varType().getText()
    varParamDefault = block.varParamDefault()

    return handle_param_varParamDefault(self, varParamDefault, block, varType)
