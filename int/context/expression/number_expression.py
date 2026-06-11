from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_FLOAT, TYPE_INT

if TYPE_CHECKING:
    from place import Place

from .common import parse_prefix_int

def handle_number_expression(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handle number, parses float(including scientific notation), hex, bin and decimal
    ||| NUMBER: FLOAT_NUMBER | HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;
    """
    text = block.NUMBER().getText().lower()

    if "." in text or "e" in text: # float or scientific notation
        return Expression(TYPE_FLOAT, float(text))
    
    return Expression(TYPE_INT, parse_prefix_int(text))