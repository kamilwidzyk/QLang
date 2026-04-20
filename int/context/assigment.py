from typing import Any, TYPE_CHECKING

from ..script_errors import ScriptErrors
from ..consts import *

if TYPE_CHECKING:
    from place import Place

def handle_assigment(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # assignStmt: ID ('[' expr ']')? '=' expr;
    var_name = block.ID().getText()

    variable = self.scopes.get(var_name)

    expr_node = block.expr()[-1] if isinstance(block.expr(), list) else block.expr()
    new_value = self.handle_block(expr_node, block)

    variable.set(new_value)

    self.scopes.set(var_name, variable)