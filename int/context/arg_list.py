from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_arg_list(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # argList: expr (',' expr)*;

    from .variable_expression import handle_variable_expression

    return [
        handle_variable_expression(self, expr, block, pos, return_variable=True)
        if isinstance(expr, VarExprCtx)
        else self.handle_block(expr, block)
        for expr in block.expr()
    ]
