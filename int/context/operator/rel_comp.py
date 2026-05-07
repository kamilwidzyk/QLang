from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place


def _value_of(item):
    return item.value if isinstance(item, Expression) else item

def handle_rel_comp(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('<' | '>' | '<=' | '>=') expr
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    result = None

    if operation == '<':
        result = _value_of(left) < _value_of(right)
    elif operation == '>':
        result = _value_of(left) > _value_of(right)
    elif operation == '<=':
        result = _value_of(left) <= _value_of(right)
    elif operation == '>=':
        result = _value_of(left) >= _value_of(right)

    return Expression(TYPE_BOOL, result)