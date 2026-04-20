from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_add_sub(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('+' | '-') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    result = None

    try:
        if operation == '+':
            result = left + right
        elif operation == '-':
            result = left - right
    except TypeError:
        self.script_errors.showError(
            pos=pos, error_type="RUNTIME ERROR", title="Type Error",
            msg=f"Cannot apply operator '{operation}' to types {type(left).__name__} and {type(right).__name__}."
        )
        exit()


    return result