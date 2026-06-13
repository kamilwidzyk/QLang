from tests.test import *

def test_errors_operators_compare_greater_equal_type_mismatch() -> bool:
    run_in_test_mode("tests\\errors\\operators\\compare\\greater_equal_type_mismatch.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=16, 
        code="OTM-1"
        ):
        return False

    return True

def test_errors_operators_compare_greater_type_mismatch() -> bool:
    run_in_test_mode("tests\\errors\\operators\\compare\\greater_type_mismatch.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=15, 
        code="OTM-2"
        ):
        return False

    return True

def test_errors_operators_compare_less_equal_type_mismatch() -> bool:
    run_in_test_mode("tests\\errors\\operators\\compare\\less_equal_type_mismatch.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=16, 
        code="OTM-3"
        ):
        return False

    return True

def test_errors_operators_compare_less_type_mismatch() -> bool:
    run_in_test_mode("tests\\errors\\operators\\compare\\less_type_mismatch.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=15, 
        code="OTM-4"
        ):
        return False

    return True
