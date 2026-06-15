# This file contains the implementation of the math operators
# Do not make calculations directly in the context, instead call the do_* 
# methods defined here to keep things consistent and to avoid code duplication


from int.context.operator.pre_post import is_variable
from int.num import Num
from int.obs import Obs, ObsRegister

from ..script_errors import ScriptErrors
from ..exception.expected_a_value import ExpectedAValueException
from ..exception.operation_not_supported import OperationNotSupportedException
from ..exception.size_error import SizeErrorException
from ..expression import *
from ..variable import Variable
from ..text import Text

def is_string_or_text(expr) -> bool:
    return ValueResolver.is_string_or_text(expr)


def _resolve_indexed_variable(expr):
    if isinstance(expr, Variable) and expr.index is not None and len(expr.index) > 0:
        return expr.get()
    return expr


def is_list(expr) -> bool:
    return ValueResolver.is_list(expr)

def is_bool(expr) -> bool:
    return ValueResolver.is_bool(expr)

def extract_string(expr) -> str:
    try:
        return ValueResolver.extract_string(expr)
    except Exception:
        raise ExpectedAValueException(ScriptErrors.Position(), "a string or text expression", code="1")
    
def extract_list(expr) -> list:
    try:
        return ValueResolver.extract_list(expr)
    except Exception:
        raise ExpectedAValueException(ScriptErrors.Position(), "a list expression", code="2")

def flatten_expressions_list(lst):
    return [x.get_value() if isinstance(x, Expression) else x for x in lst]


def _extract_scalar_value(value):
    raw = ValueResolver.resolve_for_operation(value)
    if isinstance(raw, bool):
        return int(raw)
    if isinstance(raw, (int, float)):
        return raw
    if isinstance(raw, Obs):
        return int(raw.get_value())
    return raw


def do_operation_bits_to_int(expr, pos: ScriptErrors.Position = None):
    pos = pos or ScriptErrors.Position()
    try:
        values = ValueResolver.extract_list(expr)
    except Exception:
        raise OperationNotSupportedException(pos, "Binary conversion requires a list of bits", code="4")

    if not isinstance(values, list):
        # code: ONS-4
        raise OperationNotSupportedException(pos, "Binary conversion requires a list of bits", code="4")

    total = 0
    for index, bit in enumerate(values):
        bit = ValueResolver.extract_raw_value(bit)
        if isinstance(bit, bool):
            bit = int(bit)
        if isinstance(bit, float):
            if int(bit) != bit:
                # code: ONS-5
                raise OperationNotSupportedException(pos, "Binary conversion requires integer bit values", code="5")
            bit = int(bit)
        if not isinstance(bit, int):
            # code: ONS-5
            raise OperationNotSupportedException(pos, "Binary conversion requires integer bit values", code="5")
        if bit not in (0, 1):
            # code: ONS-7
            raise OperationNotSupportedException(pos, "Binary conversion requires bits to be 0 or 1", code="7")

        total |= bit << index

    return Expression(TYPE_INT, total)


def do_operation_int_to_bits(expr, size: int, pos: ScriptErrors.Position = None):
    pos = pos or ScriptErrors.Position()
    value = ValueResolver.resolve_for_operation(expr)

    if isinstance(value, bool):
        value = int(value)
    if isinstance(value, float):
        if int(value) != value:
            # code: ONS-8
            raise OperationNotSupportedException(pos, "Binary conversion requires an integer source value", code="8")
        value = int(value)

    if not isinstance(value, int):
        # code: ONS-8
        raise OperationNotSupportedException(pos, "Binary conversion requires an integer source value", code="8")
    if size < 0:
        # code: SE-3
        raise SizeErrorException(pos, code="1")

    bits = [(value >> i) & 1 for i in range(size)]
    return Expression(TYPE_LIST, bits, shape=[size])


def _list_shape(values):
    if not isinstance(values, list):
        return []
    if len(values) == 0:
        return [0]

    def item_shape(item):
        if isinstance(item, Expression) and item.type == TYPE_LIST:
            if isinstance(item.shape, list):
                return item.shape
            if isinstance(item.shape, int):
                return [item.shape]
            return []
        if isinstance(item, list):
            return _list_shape(item)
        return []

    first_shape = item_shape(values[0])
    for element in values[1:]:
        if item_shape(element) != first_shape:
            return None
    return [len(values)] + first_shape

# FLOAT CAST
def do_operation_float_cast(left, pos: ScriptErrors.Position = None): # left.0
    pos = pos or ScriptErrors.Position()
    val = ValueResolver.resolve_for_operation(left)
    try:
        return Expression(TYPE_FLOAT, float(val))
    except (ValueError, TypeError):
        # code: ONS-11
        raise OperationNotSupportedException(pos, "Float conversion (.0) requires a numeric value", code="11")

# NOT
def do_operation_not(right): # !right
    if right.type == TYPE_BOOL:
        if right.value == True:
            return Expression(TYPE_BOOL, False)
        else:
            return Expression(TYPE_BOOL, True)
    
    return Expression(right.type, 1 if right.value == 0 else 0)

# MINUS
def do_operation_minus(right): # -right
    if right.type == TYPE_BOOL:
        return do_operation_not(right)
    

    return Expression(right.type, -(right.extract_value()))

# PLUS
def do_operation_plus(right): # +right
    return right

def convert_value(value):
    if isinstance(value, Variable):
        value = value.get_value()
    return ValueResolver.convert_value(value)

def force_to_string(value, inside_list=False):
    if isinstance(value, list):
        return '[' + ', '.join(force_to_string(item, inside_list=True) for item in value) + ']'
    if isinstance(value, Obs):
        return 'T' if value.get_value() else 'F'
    if isinstance(value, bool):
        return 'T' if value else 'F'
    if isinstance(value, str):
        if inside_list:
            return '"' + value + '"'
        return value
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, Num):
        return str(value.get_value())
    if isinstance(value, Text):
        if inside_list:
            return '"' + value.get_value() + '"'
        return value.get_value()
    if isinstance(value, Expression):
        return force_to_string(value.get_value(), inside_list=inside_list)
    return str(value)

# ADD
def do_operation_add(left, right): # left + right
    def make_list_str(x):
        list_str = ", ".join(make_list_str(x) if isinstance(x, list) else str(x) for x in x)
        return "[" + list_str + "]"
    
    if is_bool(left):
        left = ValueResolver.extract_raw_value(left)
        left = Expression(TYPE_INT, 1 if left else 0)

    if is_bool(right):
        right = ValueResolver.extract_raw_value(right)
        right = Expression(TYPE_INT, 1 if right else 0)

    
    
    if is_string_or_text(left) and is_list(right):
        # string + list
        left_str = extract_string(left)
        right_list = extract_list(right)
        converted_list = convert_value(right_list)
        flat_list = flatten_expressions_list(converted_list)
        list_str = force_to_string(flat_list)
        result = left_str + list_str
        return Expression(TYPE_STRING, result)
    
    if is_string_or_text(right) and is_list(left):
        # list + string
        right_str = extract_string(right)
        left_list = extract_list(left)
        converted_list = convert_value(left_list)
        flat_list = flatten_expressions_list(converted_list)
        list_str = force_to_string(flat_list)
        result = list_str + right_str
        return Expression(TYPE_STRING, result)

    if is_list(left):
        left_list = extract_list(left)
        if is_list(right):
            right_list = extract_list(right)
            combined = left_list + right_list
        else:
            right_val = ValueResolver.resolve_for_operation(right)
            combined = left_list + [right_val]
        return Expression(TYPE_LIST, combined, shape=_list_shape(combined))

    if is_string_or_text(left) and hasattr(right, 'get_value'):
        # string + other
        left_str = extract_string(left)
        right_val = force_to_string(right.get_value())
        result = left_str + right_val
        return Expression(TYPE_STRING, result)
    
    if is_string_or_text(right) and hasattr(left, 'get_value'):
        # other + string
        right_str = extract_string(right)
        left_val = force_to_string(left.get_value())
        result = left_val + right_str
        return Expression(TYPE_STRING, result)
    
    if is_string_or_text(left) or is_string_or_text(right):
        # String concatenation
        left_str = ValueResolver.extract_string(left)
        right_str = ValueResolver.extract_string(right)
        return Expression(TYPE_STRING, left_str + right_str)
    
    result_type = get_max_type(left, right)
    return Expression(result_type, left.get_value() + right.get_value())

# SUB
def do_operation_sub(left, right): # left - right
    if is_bool(left):
        left = ValueResolver.extract_raw_value(left)
        left = Expression(TYPE_INT, 1 if left else 0)

    if is_bool(right):
        right = ValueResolver.extract_raw_value(right)
        right = Expression(TYPE_INT, 1 if right else 0)


    if is_string_or_text(left) and is_string_or_text(right):
        # String subtraction: remove characters
        left_str = extract_string(left) 
        right_str = extract_string(right)
        for char in right_str:
            left_str = left_str.replace(char, '')
        return Expression(TYPE_STRING, left_str)
    
    result_type = get_max_type(left, right)
    return Expression(result_type, left.get_value() - right.get_value())

# MUL
def do_operation_mul(left, right): # left * right
    if is_string_or_text(left) and right.type == TYPE_INT:
        # String repetition
        left_str = extract_string(left)
        count = int(right.value) if right.value is not None else 0
        return Expression(TYPE_STRING, left_str * count)
    
    result_type = get_max_type(left, right)
    return Expression(result_type, left.get_value() * right.get_value())

# MOD
def do_operation_mod(left, right): # left % right
    def _unwrap_format_value(value):
        if isinstance(value, Expression):
            return value.extract_raw_value()
        if hasattr(value, 'extract_raw_value'):
            return value.extract_raw_value()
        if hasattr(value, 'get_value'):
            try:
                return value.get_value()
            except Exception:
                pass
        return value

    if is_string_or_text(left) and is_list(right):
        left_str = extract_string(left)
        right_list = extract_list(right)
        formatted = tuple(_unwrap_format_value(v) for v in right_list)
        result = left_str % formatted
        return Expression(TYPE_STRING, result)
    elif is_string_or_text(left):
        left_str = extract_string(left)
        right_val = _unwrap_format_value(right)
        if isinstance(right_val, list):
            right_val = tuple(_unwrap_format_value(v) for v in right_val)
        result = left_str % right_val
        return Expression(TYPE_STRING, result)

    result_type = get_max_type(left, right)

    if hasattr(left, 'get_value'):
        left = left.get_value()
    if hasattr(right, 'get_value'):
        right = right.get_value()

    return Expression(result_type, left % right)

# DIV
def do_operation_div(left, right): # left / right
    if left.type == TYPE_TEXT:
        # String split
        left_str = str(left.value) if left.value is not None else ""
        sep = str(right.value) if right.value is not None else ""
        split_result = left_str.split(sep)
        return Expression(TYPE_LIST, split_result, shape=[len(split_result)])
    
    result = left.get_value() / right.get_value()
    result_type = TYPE_FLOAT
    if isinstance(result, int) or int(result) == result:
        result_type = TYPE_INT
    return Expression(result_type, result)

# DIV INT
def do_operation_div_int(left, right): # left // right
    return Expression(TYPE_INT, left.get_value() // right.get_value())

# POW
def do_operation_pow(left, right): # left ** right
    result_type = get_max_type(left, right)
    right_val = right.get_value()
    if right_val < 0:
        result_type = TYPE_FLOAT
    return Expression(result_type, left.get_value() ** right_val)


# AND 
def do_operation_and(left, right): # left && right
    if is_bool(left):
        left = ValueResolver.extract_raw_value(left)
        left = Expression(TYPE_INT, 1 if left else 0)

    if is_bool(right):
        right = ValueResolver.extract_raw_value(right)
        right = Expression(TYPE_INT, 1 if right else 0)
        
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        return Expression(TYPE_BOOL, bool(left.get_value()) and bool(right.get_value()))
    return Expression(TYPE_BOOL, bool(left) and bool(right))

    return Expression(result_type, 1 if (left.value > 0) and (right.value > 0) else 0)

# OR
def do_operation_or(left, right): # left || right
    if is_bool(left):
        left = ValueResolver.extract_raw_value(left)
        left = Expression(TYPE_INT, 1 if left else 0)

    if is_bool(right):
        right = ValueResolver.extract_raw_value(right)
        right = Expression(TYPE_INT, 1 if right else 0)

    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        return Expression(TYPE_BOOL, bool(left.get_value()) or bool(right.get_value()))
    return Expression(TYPE_BOOL, bool(left) or bool(right))

