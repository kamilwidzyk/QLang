


from ..expression import *

from ..exception.operator_type_mismatch import OperatorTypeMismatchException
from ..script_errors import ScriptErrors

def do_compare_greater_equal(left, right, pos):
    try:
        return Expression(TYPE_BOOL, left >= right)
    except TypeError:
        # code OTM-1
        raise OperatorTypeMismatchException(
            pos=pos,
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator=">=",
            operator_worded="greater or equal",
            code="1"
        )

def do_compare_greater(left, right, pos):
    try:
        return Expression(TYPE_BOOL, left > right)
    except TypeError:
        # code OTM-2
        raise OperatorTypeMismatchException(
            pos=pos,
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator=">",
            operator_worded="greater",
            code="2"
        )

def do_compare_less_equal(left, right, pos):
    try:
        return Expression(TYPE_BOOL, left <= right)
    except TypeError:
        # code OTM-3
        raise OperatorTypeMismatchException(
            pos=pos,
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator="<=",
            operator_worded="less or equal",
            code="3"
        )

def do_compare_less(left, right, pos):
    try:
        return Expression(TYPE_BOOL, left < right)
    except TypeError:
        # code OTM-4
        raise OperatorTypeMismatchException(
            pos=pos,
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator="<",
            operator_worded="less",
            code="4"
        )

def do_compare_equal(left, right, pos):
    try:
        return Expression(TYPE_BOOL, left == right)
    except TypeError:
        # code OTM-5
        raise OperatorTypeMismatchException(
            pos=pos,
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator="==",
            operator_worded="equal",
            code="5"
        )

def do_compare_not_equal(left, right, pos):
    try:
        return Expression(TYPE_BOOL, left != right)
    except TypeError:
        # code OTM-6
        raise OperatorTypeMismatchException(
            pos=pos,
            left_type=type(left).__name__,
            right_type=type(right).__name__,
            operator="!=",
            operator_worded="not equal",
            code="6"
        )