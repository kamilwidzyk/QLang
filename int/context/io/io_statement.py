from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

from ...expression import *

if TYPE_CHECKING:
    from place import Place

from .print import handle_print
from .debug import handle_debug
from .input import handle_input

def handle_io_statement(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles IO operations: print, println, input, debug
    |||
    |||
    ||| INPUT '(' ID ('[' expr ']')? (',' format)? (',' constraint)? ')'
    ||| DEBUG '(' expr ')'
    """
    stmt_type = block.getChild(0).getText()

    if stmt_type == "print":
        handle_print(self, block, add_newline=False)
    elif stmt_type == "println":
        handle_print(self, block, add_newline=True)
    elif stmt_type == "debug":
        handle_debug(self, block)
    elif stmt_type == "input":
        handle_input(self, block, parent, pos)
