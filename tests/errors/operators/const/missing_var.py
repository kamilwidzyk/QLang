from tests.test import *

def test_errors_operators_const_missing_variable() -> bool:
    run_in_test_mode("tests\\errors\\operators\\const\\missing_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=7, 
        col_end=11, 
        code="CFV-10"
        ):
        return False

    return True

