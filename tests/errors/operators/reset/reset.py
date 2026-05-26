from tests.test import *

def test_errors_operators_reset_undefined_variable() -> bool:
    run_in_test_mode("tests\\errors\\operators\\reset\\undefined_variable.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=7, 
        col_end=8, 
        code="CFV-8"
        ):
        return False

    return True

