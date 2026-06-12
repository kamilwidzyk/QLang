from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *
from ...expression import Expression, TYPE_BOOL
from ...operations.compare import do_compare_greater, do_compare_greater_equal, do_compare_less, do_compare_less_equal

if TYPE_CHECKING:
    from place import Place


def _value_of(item):
    if hasattr(item, 'get_value'):
        return _value_of(item.get_value())
    elif hasattr(item, 'get'):
        return  _value_of(item.get())
    else:
        return item

def handle_rel_comp(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles relational comparison operations
    ||| expr ('<' | '>' | '<=' | '>=') expr
    Calculations are performed using do_compare_less, do_compare_greater, do_compare_less_equal, do_compare_greater_equal
    """
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    result = None

    if operation == '<':
        result = do_compare_less(_value_of(left), _value_of(right), pos)
    elif operation == '>':
        result = do_compare_greater(_value_of(left), _value_of(right), pos)
    elif operation == '<=':
        result = do_compare_less_equal(_value_of(left), _value_of(right), pos)
    elif operation == '>=':
        result = do_compare_greater_equal(_value_of(left), _value_of(right), pos)

    return Expression(TYPE_BOOL, result)