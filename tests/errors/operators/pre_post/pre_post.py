from tests.test import *

def test_errors_operators_post_decrement() -> bool:
    run_in_test_mode("tests\\errors\\operators\\pre_post\\post_dec.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=1, 
        col_end=2, 
        code="ATE-10"
        ):
        return False

    return True

def test_errors_operators_post_increment() -> bool:
    run_in_test_mode("tests\\errors\\operators\\pre_post\\post_inc.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=1, 
        col_end=2, 
        code="ATE-12"
        ):
        return False

    return True



def test_errors_operators_pre_decrement() -> bool:
    run_in_test_mode("tests\\errors\\operators\\pre_post\\pre_dec.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=3, 
        col_end=4, 
        code="ATE-9"
        ):
        return False

    return True

def test_errors_operators_pre_increment() -> bool:
    run_in_test_mode("tests\\errors\\operators\\pre_post\\pre_inc.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=3, 
        col_end=4, 
        code="ATE-11"
        ):
        return False

    return True