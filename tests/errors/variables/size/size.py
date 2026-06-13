from tests.test import *


def test_errors_variable_size_not_int() -> bool:
    run_in_test_mode("tests\\errors\\variables\\size\\size_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=12, 
        col_end=17, 
        code="SE-1"
        ):
        return False

    return True

def test_errors_variable_size_negative() -> bool:
    run_in_test_mode("tests\\errors\\variables\\size\\size_negative.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=12, 
        col_end=16, 
        code="SE-2"
        ):
        return False

    return True