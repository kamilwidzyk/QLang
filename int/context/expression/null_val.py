from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...expression import Expression, TYPE_TEXT

if TYPE_CHECKING:
    from place import Place

def handle_null(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # NULL: 'NULL';
    return Expression(TYPE_TEXT, "\0")