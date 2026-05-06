from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..function import FunctionParam

if TYPE_CHECKING:
    from place import Place

def handle_param(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # param: (STATE | OBS | NUM) ID ('[' NUMBER ']')?;

    # Get param type
    param_type = None
    if block.STATE():
        param_type = "STATE"
    elif block.OBS():
        param_type = "OBS"
    elif block.NUM():
        param_type = "NUM"

    param_name = block.ID().getText()
    param_size = None
    if block.NUMBER():
        param_size = int(block.NUMBER().getText())
        # NUM params cannot be arrays
        if param_type == "NUM":
            self.script_errors.showError(
                pos=pos,
                error_type="SYNTAX ERROR",
                title="Unsupported num array param",
                msg=f"Parameter '{param_name}': num parameters cannot be arrays. Use a plain 'num' param."
            )
            exit()
        # check if the param size > 0
        if param_size <= 0:
            self.script_errors.showError(
                pos=pos,
                error_type="SYNTAX ERROR",
                title="Negative size",
                msg="I'm not capable of managing your imaginary, negative-sized arrays."
            )
            exit()

    return FunctionParam(name=param_name, type=param_type, size=param_size)