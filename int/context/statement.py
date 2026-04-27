from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import * 
from .function.function_call import FunctionReturn
from ..QLang.QLangParser import QLangParser

if TYPE_CHECKING:
    from place import Place

def handle_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    def is_return(block) -> bool:
        if not isinstance(block, TerminalCtx):
            return False
        if block.getText() != "return":
            return False
        return True
    
    if is_return(block.getChild(0)):
        return_val = self.handle_block(block.getChild(1))
        raise FunctionReturn(return_val)
    
    self.handle_block(block.getChild(0), parent=block)

    return None