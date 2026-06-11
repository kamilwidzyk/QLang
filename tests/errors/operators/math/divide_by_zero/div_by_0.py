from tests.test import *

def test_errors_operators_math_divide_by_zero() -> bool:
    run_in_test_mode("tests\\errors\\operators\\math\\divide_by_zero\\div_by_0.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=14, 
        col_end=15, 
        code="DBZ-2"
        ):
        return False

    return True

def test_errors_operators_math_divide_eq_zero() -> bool:
    run_in_test_mode("tests\\errors\\operators\\math\\divide_by_zero\\div_eq_0.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=6, 
        col_end=7, 
        code="DBZ-1"
        ):
        return False

    return True

