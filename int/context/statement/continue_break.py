from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from .statement import BreakLoop, ContinueLoop

if TYPE_CHECKING:
    from place import Place


def handle_continue(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles continue statement
    Raises ContinueLoop exception

    """
    print("Continue")
    raise ContinueLoop()

def handle_break(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles break statement
    Raises BreakLoop exception

    """
    print("Break")
    raise BreakLoop()