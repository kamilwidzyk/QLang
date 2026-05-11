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

    # TODO: Check types before the operation

    if operation == '*':
        return do_operation_mul(left, right)

    if operation == '/':
        if is_text_or_string(left) and is_text_or_string(right):
            left_str = extract_string(left)
            right_str = extract_string(right)

            result = left_str.split(right_str)

            return Expression(TYPE_LIST, [Expression(TYPE_STRING, item) for item in result], shape=[len(result)])

        if right == 0:
            self.script_errors.showError(pos, "RUNTIME ERROR", "Math Error","I don't do division by zero. Nobody does.")
            exit()

        if left.type == TYPE_INT and right.type == TYPE_INT:
            return do_operation_div_int(left, right)
        
        return do_operation_div(left, right)


    if operation == '%':
        return do_operation_mod(left, right)
        # string formatting: STRING % LIST
        if isinstance(left, Expression) and (left.type in [TYPE_STRING, TYPE_TEXT]) and isinstance(right, Expression) and right.type in [TYPE_LIST]:
            left_str = left.value if left.type == TYPE_STRING else left.value.get()
            right_list = right.value if right.type == TYPE_LIST else right.value.get()
            return Expression(TYPE_STRING, left_str % tuple([x.value for x in right_list]))
        else:
            # Numeric modulo
            
            return do_operation_mod(left, right)
