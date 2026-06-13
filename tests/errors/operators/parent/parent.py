from tests.test import *

def test_errors_operators_parent_undefined_variable() -> bool:
    run_in_test_mode("tests\\errors\\operators\\parent\\undefined_variable.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=14, 
        col_end=15, 
        code="CFV-6"
        ):
        return False

    return True

def test_errors_operators_parent_too_much() -> bool:
    run_in_test_mode("tests\\errors\\operators\\parent\\too_much.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=5, 
        col_end=8, 
        code="NPS-2"
        ):
        return False

    return True
