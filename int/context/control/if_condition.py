from __future__ import annotations
from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *

if TYPE_CHECKING:
    from place import Place

from .common import check_condition


def _if_bodies(block: Any) -> list:
    """
    Returns a list of bodies of if/elif/else 
    Both block { code... } and single statements are supported as body.
    """
    bodies = []
    for child in getattr(block, 'children', []):
        if isinstance(child, (BlockCtx, StatementCtx)):
            bodies.append(child)
    return bodies

def _choose_body(conditions: list, bodies: list, pos) -> Any:
    """
    Chooses which body of if/elif/else to execute based on the conditions.
    Returns the chosen body or None if no condition is satisfied and there is no else block.
    """
    for cond, body in zip(conditions, bodies):
        #print("Condition: ", cond.get_value())
        if check_condition(cond, pos):
            #print("Condition satisfied, executing body")
            return body
        #print("Condition not satisfied, checking next condition")

    # If no condition is satisfied, but there is an else block, select it
    if len(bodies) > len(conditions):
        return bodies[-1]

    # If there is no satisfied condition and no else block, return None
    return None


def handle_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles if statement.
    ||| ifStmt: IF '(' expr ')' (block | statement) ((ELSE_IF | ELIF) '(' expr ')' (block | statement))* (ELSE (block | statement))?;

    if (<condition>) <body>

    if (<condition>) <body>
    elif (condition) <body>
    else if (<condition>) <body>
    else <body>

    <body> can be either a block { code... } or a single statement
    elif is short for else if

    """
    conditions = [self.handle_block(expr, block) for expr in block.expr()]
    bodies = _if_bodies(block)
    chosen_body = _choose_body(conditions, bodies, pos)

    # If there is no satisfied condition and no else block, do nothing
    if chosen_body is None:
        return

    # Start new scope
    self.scopes.push(pos, scope_type="if")
    try:
        self.execute_block(chosen_body, parent=block)
    finally:
        # Pop the scope after running the block
        self.scopes.pop()


def handle_short_if(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Ternary operator
    ||| shortIfStmt: expr '?' expr ':' expr;

    num x = condition ? valueIfTrue : valueIfFalse;

    """
    expressions = [x for x in block.expr()]

    # check the condition and return valueIfTrue if condition is satisfied, otherwise return valueIfFalse    
    condition = self.handle_block(expressions[0], block)
    if check_condition(condition, pos):
        return self.handle_block(expressions[1], block)
    else:
        return self.handle_block(expressions[2], block)