from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *
from ..obs import Obs, ObsRegister

if TYPE_CHECKING:
    from place import Place

def handle_place_member(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handle place member
    Just execute everything in it
    """
    for child in block.getChildren():
        self.handle_block(child, parent=block)