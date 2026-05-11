


from ..expression import *
from .operators import extract_list, extract_string, is_string_or_text


def do_compare_greater_equal(left, right):
    if is_string_or_text(left) and is_string_or_text(right):
        left_str = extract_string(left)
        right_str = extract_string(right)
        return Expression(TYPE_BOOL, left_str >= right_str)
    return Expression(TYPE_BOOL, left.value >= right.value)

def do_compare_greater(left, right):
    if is_string_or_text(left) and is_string_or_text(right):
        left_str = extract_string(left)
        right_str = extract_string(right)
        return Expression(TYPE_BOOL, left_str > right_str)
    return Expression(TYPE_BOOL, left.value > right.value)

def do_compare_less_equal(left, right):
    if is_string_or_text(left) and is_string_or_text(right):
        left_str = extract_string(left)
        right_str = extract_string(right)
        return Expression(TYPE_BOOL, left_str <= right_str)
    return Expression(TYPE_BOOL, left.value <= right.value)

def do_compare_less(left, right):
    if is_string_or_text(left) and is_string_or_text(right):
        left_str = extract_string(left)
        right_str = extract_string(right)
        return Expression(TYPE_BOOL, left_str < right_str)
    return Expression(TYPE_BOOL, left.value < right.value)

def do_compare_equal(left, right):
    if is_string_or_text(left) and is_string_or_text(right):
        left_str = extract_string(left)
        right_str = extract_string(right)
        return Expression(TYPE_BOOL, left_str == right_str)
    return Expression(TYPE_BOOL, left.value == right.value)

def do_compare_not_equal(left, right):
    if is_string_or_text(left) and is_string_or_text(right):
        left_str = extract_string(left)
        right_str = extract_string(right)
        return Expression(TYPE_BOOL, left_str != right_str)
    return Expression(TYPE_BOOL, left.value != right.value)
