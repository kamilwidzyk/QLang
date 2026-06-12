from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import TerminalCtx
from .function.function_call import FunctionReturn

if TYPE_CHECKING:
    from place import Place


class BreakLoop(Exception):
    pass


class ContinueLoop(Exception):
    pass


def handle_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles any statement
    Raises returns, breaks and continues
    """
    def is_return(block) -> bool:
        if not isinstance(block, TerminalCtx):
            return False
        if block.getText() != "return":
            return False
        return True
    
    first = block.getChild(0)

    # return
    if is_return(first):
        return_val = None
        if block.getChildCount() > 2:
            return_val = self.handle_block(block.getChild(1))
        raise FunctionReturn(return_val)

    # break
    if isinstance(first, TerminalCtx) and first.getText() == "break":
        raise BreakLoop()

    # continue
    if isinstance(first, TerminalCtx) and first.getText() == "continue":
        raise ContinueLoop()

    if isinstance(first, TerminalCtx) and first.getText() == "{":
        for item in self.handle_block(first, parent=block):
            self.handle_block(item, parent=block)
        return None

    self.handle_block(first, parent=block)

    return None