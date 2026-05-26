from tests.test import *


def test_errors_variable_non_existing() -> bool:
    run_in_test_mode("tests\\errors\\variables\\missing_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=9, 
        col_end=25, 
        code="CFV-3"
        ):
        return False

    return True

def test_errors_variable_non_existing2() -> bool:
    run_in_test_mode("tests\\errors\\variables\\missing_var2.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=8, 
        line_end=8, 
        col_start=9, 
        col_end=11, 
        code="CFV-3"
        ):
        return False

    return True