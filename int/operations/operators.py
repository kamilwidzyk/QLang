# This file contains the implementation of the math operators
# Do not make calculations directly in the context, instead call the do_* 
# methods defined here to keep things consistent and to avoid code duplication


from int.exception.modulo_over_zero import ModuloOverZeroException
from int.context.operator.pre_post import is_variable
from int.script_errors import ScriptErrors
from int.exception.assignment_to_expression import AssignmentToExpressionException

from ..expression import *
from ..variable import Variable
from ..text import Text

def is_string_or_text(expr) -> bool:
    return (isinstance(expr, Expression) and expr.type in [TYPE_STRING, TYPE_TEXT]) \
        or isinstance(expr, Text) or (isinstance(expr, Variable) and expr.type == TYPE_TEXT)

def is_list(expr) -> bool:
    return (isinstance(expr, Expression) and expr.type == TYPE_LIST) \
        or (isinstance(expr, Variable) and expr.type in [TYPE_LIST, TYPE_ARRAY]) \
        or (hasattr(expr, 'data') and isinstance(expr.data, list))

def extract_string(expr) -> str:
    if isinstance(expr, Expression) and expr.type in [TYPE_STRING, TYPE_TEXT]:
        return expr.value if expr.type == TYPE_STRING else expr.value.get()
    elif isinstance(expr, Text):
        return expr.get()
    elif isinstance(expr, Variable) and expr.type == TYPE_TEXT:
        return expr.data.get()
    else:
        raise ValueError("Expected a string or text expression")
    
def extract_list(expr) -> list:
    if isinstance(expr, Expression) and expr.type == TYPE_LIST:
        return expr.value
    elif isinstance(expr, Variable) and expr.type in [TYPE_LIST, TYPE_ARRAY]:
        return expr.data
    elif hasattr(expr, 'data') and isinstance(expr.data, list):
        return expr.data
    else:
        raise ValueError("Expected a list expression")

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
    

    return Expression(right.type, -right.value)

# PLUS
def do_operation_plus(right): # +right
    return right

# ADD
def do_operation_add(left, right): # left + right
    if left.type == TYPE_TEXT or right.type == TYPE_TEXT:
        # String concatenation
        left_str = str(left.value) if left.value is not None else ""
        right_str = str(right.value) if right.value is not None else ""
        return Expression(TYPE_TEXT, left_str + right_str)
    
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value + right.value)

# SUB
def do_operation_sub(left, right): # left - right
    if left.type == TYPE_TEXT or right.type == TYPE_TEXT:
        # String subtraction: remove characters
        left_str = str(left.value) if left.value is not None else ""
        right_str = str(right.value) if right.value is not None else ""
        for char in right_str:
            left_str = left_str.replace(char, '')
        return Expression(TYPE_TEXT, left_str)
    
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value - right.value)

# MUL
def do_operation_mul(left, right): # left * right
    if is_string_or_text(left) and right.type == TYPE_INT:
        # String repetition
        left_str = extract_string(left)
        count = int(right.value) if right.value is not None else 0
        return Expression(TYPE_TEXT, left_str * count)
    
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value * right.value)

# MOD
def do_operation_mod(left, right): # left % right
    if is_string_or_text(left) and is_list(right):
        left_str = extract_string(left)
        right_list = extract_list(right)
        result = left_str % tuple([x.value for x in right_list])
        return Expression(TYPE_STRING, result)
    
    if right == 0:
        raise ModuloOverZeroException(ScriptErrors.Position.UNKNOWN)

    if not is_variable(left):
        raise AssignmentToExpressionException(ScriptErrors.Position.UNKNOWN)

    result_type = get_max_type(left, right)
    return Expression(result_type, left.value % right.value)

# DIV
def do_operation_div(left, right): # left / right
    if left.type == TYPE_TEXT:
        # String split
        left_str = str(left.value) if left.value is not None else ""
        sep = str(right.value) if right.value is not None else ""
        split_result = left_str.split(sep)
        return Expression(TYPE_LIST, split_result)
    
    result = left.value / right.value
    result_type = TYPE_FLOAT
    if isinstance(result, int) or int(result) == result:
        result_type = TYPE_INT
    return Expression(result_type, result)

# DIV INT
def do_operation_div_int(left, right): # left // right
    return Expression(TYPE_INT, left.value // right.value)

# POW
def do_operation_pow(left, right): # left ** right
    result_type = get_max_type(left, right)
    if(right.value < 0):
        result_type = TYPE_FLOAT
    return Expression(result_type, left.value ** right.value)


# AND 
def do_operation_and(left, right): # left && right
    if left.type == TYPE_BOOL and right.type == TYPE_BOOL:
        return Expression(TYPE_BOOL, (left.value == True) and (right.value == True))
    
    result_type = get_max_type(left, right)
    print(result_type)

    return Expression(result_type, 1 if (left.value > 0) and (right.value > 0) else 0)

# OR
def do_operation_or(left, right): # left || right
    if left.type == TYPE_BOOL and right.type == TYPE_BOOL:
        return Expression(TYPE_BOOL, (left.value == True) or (right.value == True))
    
    result_type = get_max_type(left, right)

    return Expression(result_type, 1 if (left.value > 0) or (right.value > 0) else 0)

