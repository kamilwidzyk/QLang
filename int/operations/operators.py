# This file contains the implementation of the math operators
# Do not make calculations directly in the context, instead call the do_* 
# methods defined here to keep things consistent and to avoid code duplication

# Functions in this file should not raise any exceptions, all error handling should be done in the context!

from ..expression import *


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
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value + right.value)

# SUB
def do_operation_sub(left, right): # left - right
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value - right.value)

# MUL
def do_operation_mul(left, right): # left * right
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value * right.value)

# MOD
def do_operation_mod(left, right): # left % right
    result_type = get_max_type(left, right)
    return Expression(result_type, left.value % right.value)

# DIV
def do_operation_div(left, right): # left / right
    result = left.value / right.value
    result_type = TYPE_FLOAT
    if isinstance(result, int) or int(result) == result:
        result_type = TYPE_INT
    return Expression(result_type, result)

# DIV INT
def do_operation_div_int(left, right): # left // right
    return Expression(TYPE_INT, left // right)

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

