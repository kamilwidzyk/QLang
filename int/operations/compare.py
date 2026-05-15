


from ..expression import *
from .operators import extract_list, extract_string, is_string_or_text


def do_compare_greater_equal(left, right):
    try:
        return Expression(TYPE_BOOL, left >= right)
    except TypeError:
        raise TypeError("Unsupported(or not implemented) types for comparison '>=': " + str(type(left).__name__) + " and " + str(type(right).__name__))

def do_compare_greater(left, right):
    try:
        return Expression(TYPE_BOOL, left > right)
    except TypeError:
        raise TypeError("Unsupported(or not implemented) types for comparison '>': " + str(type(left).__name__) + " and " + str(type(right).__name__))

def do_compare_less_equal(left, right):
    try:
        return Expression(TYPE_BOOL, left <= right)
    except TypeError:
        raise TypeError("Unsupported(or not implemented) types for comparison '<=': " + str(type(left).__name__) + " and " + str(type(right).__name__))

def do_compare_less(left, right):
    try:
        return Expression(TYPE_BOOL, left < right)
    except TypeError:
        raise TypeError("Unsupported(or not implemented) types for comparison '<': " + str(type(left).__name__) + " and " + str(type(right).__name__))

def do_compare_equal(left, right):
    try:
        return Expression(TYPE_BOOL, left == right)
    except TypeError:
        raise TypeError("Unsupported(or not implemented) types for comparison '==': " + str(type(left).__name__) + " and " + str(type(right).__name__))

def do_compare_not_equal(left, right):
    try:
        return Expression(TYPE_BOOL, left != right)
    except TypeError:
        raise TypeError("Unsupported(or not implemented) types for comparison '!=': " + str(type(left).__name__) + " and " + str(type(right).__name__))