from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_string(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # STRING     : '"' (~["\r\n])* '"' ;
    return [x for x in block.getChildren()][0].getText()[1:-1]