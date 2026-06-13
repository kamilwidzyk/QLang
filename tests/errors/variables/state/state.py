from tests.test import *


def test_errors_variable_state_print() -> bool:
    run_in_test_mode("tests\\errors\\variables\\state\\print_state.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=7, 
        col_end=8, 
        code="DQA-2"
        ):
        return False

    return True

def test_errors_variable_state_paren() -> bool:
    run_in_test_mode("tests\\errors\\variables\\state\\paren_state.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=8, 
        col_end=9, 
        code="DQA-2"
        ):
        return False

    return True

def test_errors_variable_state_assign() -> bool:
    run_in_test_mode("tests\\errors\\variables\\state\\assign.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=7, 
        code="DQA-5"
        ):
        return False

    return True

def test_errors_variable_state_expr_assign() -> bool:
    run_in_test_mode("tests\\errors\\variables\\state\\expr_assign.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=7, 
        col_end=13, 
        code="DQA-6"
        ):
        return False

    return True

def test_errors_variable_state_initial_assign() -> bool:
    run_in_test_mode("tests\\errors\\variables\\state\\initial_assign.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=11, 
        col_end=13, 
        code="DQA-7"
        ):
        return False

    return True

def test_errors_variable_const_state() -> bool:
    run_in_test_mode("tests\\errors\\variables\\state\\const_state.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=7, 
        col_end=12, 
        code="ONS-1"
        ):
        return False

    return True