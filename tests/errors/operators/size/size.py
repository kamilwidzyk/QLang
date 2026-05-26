from tests.test import *

def test_errors_size_undefined_variable() -> bool:
    run_in_test_mode("tests\\errors\\operators\\size\\undefined_variable.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=10, 
        col_end=13, 
        code="CFV-1"
        ):
        return False

    return True