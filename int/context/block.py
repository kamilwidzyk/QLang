from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_block_ctx(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles block of code
    ||| block: '{' statement* '}';
    Just return statements inside
    """
    return block.statement()