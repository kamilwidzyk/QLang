from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.compare import do_compare_greater
from ...expression import Expression, TYPE_INT, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place

def check_condition(expr_block):
    if expr_block.type == TYPE_BOOL:
        return expr_block.value == True
    
    return do_compare_greater(expr_block, Expression(TYPE_INT, 0))

def handle_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # ifStmt: IF '(' expr=if_expr ')' block=if_block ((ELSE_IF | ELIF) '(' expr=elif_expr ')' block=elif_block)* (ELSE block=else_block)?;

    if check_condition(self.handle_block(block.expr(0), block)):
        chosen_block = block.block(0)
    else:
        chosen_block = None

        expr_count = len(block.expr())
        for i in range(1, expr_count):
            if check_condition(self.handle_block(block.expr(i), block)):
                chosen_block = block.block(i)
                break

        if chosen_block is None:
            total_blocks = len(block.block())
            total_conditions = expr_count

            if total_blocks > total_conditions:
                chosen_block = block.block(total_blocks - 1)

    if chosen_block is None:
        return

    self.scopes.push(pos, scope_type="if")
    try:
        for item in self.handle_block(chosen_block, block):
            self.handle_block(item, parent=chosen_block)
    finally:
        self.scopes.pop()

def handle_short_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # shortIfStmt: expr '?' expr ':' expr;

    expressions = [x for x in block.expr()]

    
    condition = self.handle_block(expressions[0], block)
    if check_condition(condition):
        return self.handle_block(expressions[1], block)
    else:
        return self.handle_block(expressions[2], block)