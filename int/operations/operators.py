# This file contains the implementation of the math operators
# Do not make calculations directly in the context, instead call the do_* 
# methods defined here to keep things consistent and to avoid code duplication

# Functions in this file should not raise any exceptions, all error handling should be done in the context!

# NOT
def do_operation_not(right): # !right
    return 1 if right == 0 else 0

# MINUS
def do_operation_minus(right): # -right
    return -right

# PLUS
def do_operation_plus(right): # +right
    return right

# ADD
def do_operation_add(left, right): # left + right
    return left + right

# SUB
def do_operation_sub(left, right): # left - right
    return left - right

# MUL
def do_operation_mul(left, right): # left * right
    return left * right

# MOD
def do_operation_mod(left, right): # left % right
    return left % right

# DIV
def do_operation_div(left, right): # left / right
    return left / right

# DIV INT
def do_operation_div_int(left, right): # left // right
    return left // right



# AND 
def do_operation_and(left, right): # left && right
    return 1 if (left > 0) and (right > 0) else 0

# OR
def do_operation_or(left, right): # left || right
    return 1 if (left > 0) or (right > 0) else 0

