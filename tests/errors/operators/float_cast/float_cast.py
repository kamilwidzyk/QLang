from tests.test import *

def test_errors_operators_float_cast_str() -> bool:
    run_in_test_mode("tests\\errors\\operators\\float_cast\\float_cast_str.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=9, 
        col_end=12, 
        code="ONS-11"
        ):
        return False

    return True
