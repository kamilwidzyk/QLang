


from ..expression import *
from .operators import extract_list, extract_string, is_string_or_text


def do_compare_greater_equal(left, right):
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        left_val = left.get_value()
        right_val = right.get_value()
        return Expression(TYPE_BOOL, left_val >= right_val)
    raise TypeError("Unsupported(or not implemented) types for comparison '>=': " + str(left.type) + " and " + str(right.type))

def do_compare_greater(left, right):
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        left_val = left.get_value()
        right_val = right.get_value()
        return Expression(TYPE_BOOL, left_val > right_val)
    raise TypeError("Unsupported(or not implemented) types for comparison '>': " + str(left.type) + " and " + str(right.type))

def do_compare_less_equal(left, right):
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        left_val = left.get_value()
        right_val = right.get_value()
        return Expression(TYPE_BOOL, left_val <= right_val)
    raise TypeError("Unsupported(or not implemented) types for comparison '<=': " + str(left.type) + " and " + str(right.type))

def do_compare_less(left, right):
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        left_val = left.get_value()
        right_val = right.get_value()
        return Expression(TYPE_BOOL, left_val < right_val)
    raise TypeError("Unsupported(or not implemented) types for comparison '<': " + str(left.type) + " and " + str(right.type))

def do_compare_equal(left, right):
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        left_val = left.get_value()
        right_val = right.get_value()
        return Expression(TYPE_BOOL, left_val == right_val)
    raise TypeError("Unsupported(or not implemented) types for comparison '==': " + str(left.type) + " and " + str(right.type))

def do_compare_not_equal(left, right):
    if hasattr(left, 'get_value') and hasattr(right, 'get_value'):
        left_val = left.get_value()
        right_val = right.get_value()
        return Expression(TYPE_BOOL, left_val != right_val)
    raise TypeError("Unsupported(or not implemented) types for comparison '!=': " + str(left.type) + " and " + str(right.type))
