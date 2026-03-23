from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_string(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # STRING     : '"' (~["\r\n])* '"' ;

    # 1. Terminal "<content>"

    if not self.has_children(block):
        print("StrExprContext: missing 'children' key or no children")
        exit()
    
    content = self.extract_text(block["children"][0], parent=block)

    if len(content) < 2:
        print("StrExprContent: content size of minimum 2 is required(empty string)")
        exit()
    
    return content[1:-1] # remove first and last characters(")
