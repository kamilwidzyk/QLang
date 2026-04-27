


from ..expression import *


def do_compare_greater_equal(left, right):
    return Expression(TYPE_BOOL, left.value >= right.value)

def do_compare_greater(left, right):
    return Expression(TYPE_BOOL, left.value > right.value)

def do_compare_less_equal(left, right):
    return Expression(TYPE_BOOL, left.value <= right.value)

def do_compare_less(left, right):
    return Expression(TYPE_BOOL, left.value < right.value)

def do_compare_equal(left, right):
    return Expression(TYPE_BOOL, left.value == right.value)

def do_compare_not_equal(left, right):
    return Expression(TYPE_BOOL, left.value != right.value)
