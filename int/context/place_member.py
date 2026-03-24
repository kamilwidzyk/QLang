from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_place_member(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    if not self.has_children(block):
        self.script_errors.showError(pos, "DEEP ERROR", "Malformed AST", "PlaceMemberContext: 'children' key missing or no children")
        exit()

    for child in block["children"]:
        self.handle_block(child, parent=block)