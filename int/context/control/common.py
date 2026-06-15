



from ...operations.compare import do_compare_greater
from int.expression import TYPE_BOOL, TYPE_INT, Expression


def check_condition(expr_block, pos) -> bool:
    """
    Checks if the condition is satisfied:
        is bool? -> is True
        else -> is > 0
    """
    if expr_block.type == TYPE_BOOL:
        return expr_block.value == True
    return do_compare_greater(expr_block, Expression(TYPE_INT, 0), pos).get_value()