from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

def handle_format(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles input format specifier
    ||| format: BIN | HEX;
    """
    return [x for x in block.getChildren()][0].getText()
