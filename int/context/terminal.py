from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_terminal(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    return block.getText()