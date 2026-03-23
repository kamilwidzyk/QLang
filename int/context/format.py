from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_format(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # format: BIN | HEX;

    if not self.has_children(block):
        print("FormatContext: missing 'children' key or no children")
        exit()

    child = block["children"][0]

    if self.is_terminal(child, text="HEX", parent=block):
        return "HEX"
    elif self.is_terminal(child, text="BIN", parent=block):
        return "BIN"
    else:
        print("FormatContext: unknown format")
        exit()