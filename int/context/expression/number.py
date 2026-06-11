from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_INT, TYPE_FLOAT

if TYPE_CHECKING:
    from place import Place

from .number_expression import handle_number_expression

def handle_expression_number(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles any number, execution passed to number_expression handler
    ||| NUMBER: FLOAT_NUMBER | HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;
    """
    # 
    return handle_number_expression(self, block, parent, pos)