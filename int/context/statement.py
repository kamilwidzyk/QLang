from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import * 

if TYPE_CHECKING:
    from place import Place

def handle_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    if "children" not in block:
        print("statementContext 'children' key missing")
        exit()

    children = block["children"]

    for child in children:
        self.handle_block(child, parent=block)
