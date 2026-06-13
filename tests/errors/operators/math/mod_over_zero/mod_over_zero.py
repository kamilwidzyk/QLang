from tests.test import *

def test_errors_operators_math_modulo_over_zero() -> bool:
    run_in_test_mode("tests\\errors\\operators\\math\\mod_over_zero\\mod_over_zero.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=6, 
        col_end=7, 
        code="MOZ-1"
        ):
        return False

    return True

def test_errors_operators_math_modulo_eq_zero() -> bool:
    run_in_test_mode("tests\\errors\\operators\\math\\mod_over_zero\\mod_eq_zero.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=6, 
        col_end=7, 
        code="MOZ-2"
        ):
        return False

    return True

