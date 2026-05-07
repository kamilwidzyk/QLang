from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression, TYPE_BOOL

if TYPE_CHECKING:
    from place import Place


def _value_of(item):
    return item.value if isinstance(item, Expression) else item

def handle_eq_comp(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('==' | '!=') expr
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    right = self.handle_block(children[2], block)

    if children[1].getText() == "==":
        return Expression(TYPE_BOOL, _value_of(left) == _value_of(right))
    else:
        return Expression(TYPE_BOOL, _value_of(left) != _value_of(right))
    