from tests.test import *

def test_errors_operators_and_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\and_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=1, 
        col_end=2, 
        code="ATE-1"
        ):
        return False

    return True

def test_errors_operators_div_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\div_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=6, 
        line_end=6, 
        col_start=1, 
        col_end=2, 
        code="ATE-3"
        ):
        return False

    return True

def test_errors_operators_minus_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\minus_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=1, 
        col_end=2, 
        code="ATE-4"
        ):
        return False

    return True

def test_errors_operators_mod_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\mod_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=6, 
        line_end=6, 
        col_start=1, 
        col_end=2, 
        code="ATE-5"
        ):
        return False

    return True

def test_errors_operators_mul_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\mul_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=7, 
        line_end=7, 
        col_start=1, 
        col_end=2, 
        code="ATE-6"
        ):
        return False

    return True

def test_errors_operators_or_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\or_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=7, 
        line_end=7, 
        col_start=1, 
        col_end=2, 
        code="ATE-2"
        ):
        return False

    return True

def test_errors_operators_plus_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\plus_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=8, 
        line_end=8, 
        col_start=1, 
        col_end=2, 
        code="ATE-7"
        ):
        return False

    return True

def test_errors_operators_pow_equal() -> bool:
    run_in_test_mode("tests\\errors\\operators\\something_equal\\pow_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=9, 
        line_end=9, 
        col_start=1, 
        col_end=2, 
        code="ATE-8"
        ):
        return False

    return True