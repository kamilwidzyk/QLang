from tests.test import *

def test_errors_function_not_declared() -> bool:
    run_in_test_mode("tests\\errors\\functions\\not_declared.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=1, 
        col_end=7, 
        code="NFTC-1"
        ):
        return False

    return True

def test_errors_function_variable_call() -> bool:
    run_in_test_mode("tests\\errors\\functions\\variable_call.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=7, 
        code="VC-1"
        ):
        return False

    return True

def test_errors_function_redeclaration() -> bool:
    run_in_test_mode("tests\\errors\\functions\\redeclaration.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=7, 
        col_start=1, 
        col_end=2, 
        code="FR-1"
        ):
        return False

    return True