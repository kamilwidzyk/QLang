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


def _if_bodies(block: Any) -> list:
    bodies = []
    for child in getattr(block, 'children', []):
        if isinstance(child, (BlockCtx, StatementCtx)):
            bodies.append(child)
    return bodies


def handle_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    conditions = [self.handle_block(expr, block) for expr in block.expr()]
    bodies = _if_bodies(block)

    chosen_block = None
    for cond, body in zip(conditions, bodies):
        if check_condition(cond):
            chosen_block = body
            break

    if chosen_block is None and len(bodies) > len(conditions):
        chosen_block = bodies[-1]

    if chosen_block is None:
        return

    self.scopes.push(pos, scope_type="if")
    try:
        if isinstance(chosen_block, BlockCtx):
            for item in self.handle_block(chosen_block, block):
                self.handle_block(item, parent=chosen_block)
        else:
            self.handle_block(chosen_block, parent=block)
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