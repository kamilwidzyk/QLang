from typing import Any, TYPE_CHECKING

from int.exception.divide_by_zero import DivideByZeroException

from ...variable import Variable

from ...script_errors import ScriptErrors
from ...consts import *

from ...operations.operators import do_operation_div
from ...operations.operators import do_operation_div_int
from ...operations.operators import do_operation_mod
from ...operations.operators import do_operation_mul
from ...expression import TYPE_INT, TYPE_TEXT, Expression, TYPE_STRING, TYPE_LIST
from ...text import Text
from ...exception.expected_a_value import ExpectedAValueException
from ...exception.modulo_over_zero import ModuloOverZeroException

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
        # code EAV-1
        raise ExpectedAValueException(ScriptErrors.Position(), "a string or text", code="1")

def handle_mul_div_mod(self: Place, block: Any, parent: Any, pos: ScriptErrors.Position):
    """
    Handles multiplication, division and modulus operations
    ||| expr ('*' | '/' | '%') expr
        Calculations are performed using do_operation_mul, do_operation_div, do_operation_div_int and do_operation_mod
        Division by zero is checked and raises DivideByZeroException with code "2" for '/'
        If either operand is text or string, only multiplication is allowed, which performs string repetition.
        In this case, the right operand must be an integer, otherwise ExpectedAValueException with code "1" is raised.
    """
    children = [x for x in block.getChildren()]
    left = self.handle_block(children[0], block)
    operation = children[1].getText()
    right = self.handle_block(children[2], block)

    if operation == '*':
        return do_operation_mul(left, right)

    if operation == '/':
        if right == 0:
            # code DBZ-2
            raise DivideByZeroException(ScriptErrors.Position.extract(children[2]), code="2")
        
        if left.type == TYPE_INT and right.type == TYPE_INT:
            return do_operation_div_int(left, right)

        return do_operation_div(left, right)

    if operation == '%':
        if not is_text_or_string(left) and right == 0:
            # code MOZ-1
            raise ModuloOverZeroException(ScriptErrors.Position.extract(children[2]), code="1")

        return do_operation_mod(left, right)
