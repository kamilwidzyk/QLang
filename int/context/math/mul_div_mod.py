from typing import Any, TYPE_CHECKING

from ...variable import Variable

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.operators import do_operation_div
from ...operations.operators import do_operation_div_int
from ...operations.operators import do_operation_mod
from ...operations.operators import do_operation_mul
from ...expression import TYPE_INT, TYPE_TEXT, Expression, TYPE_STRING, TYPE_LIST
from ...text import Text

if TYPE_CHECKING:
    from place import Place

def is_text_or_string(expr) -> bool:
    return (isinstance(expr, Expression) and expr.type in [TYPE_TEXT, TYPE_STRING]) \
        or isinstance(expr, Text) or (isinstance(expr, Variable) and expr.type == TYPE_TEXT)

def extract_string(expr) -> str:
    if isinstance(expr, Expression) and expr.type in [TYPE_TEXT, TYPE_STRING]:
        return expr.value if expr.type == TYPE_STRING else expr.value.get()
    elif isinstance(expr, Text):
        return expr.get()
    elif isinstance(expr, Variable) and expr.type == TYPE_TEXT:
        return expr.data.get()
    else:
        raise ValueError("Expected a string or text expression")

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    # expr ('*' | '/' | '%') expr 
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    if operation == '*':
        return left * right

    if operation == '/':
        return left / right

    if operation == '%':
        return left % right
