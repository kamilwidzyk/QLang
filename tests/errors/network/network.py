from tests.test import *


def test_errors_network_receive_size_not_int() -> bool:
    run_in_test_mode("tests\\errors\\network\\receive_size_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=6, 
        col_end=11, 
        code="PSNI-1"
        ):
        return False

    return True

def test_errors_network_receive_size_negative() -> bool:
    run_in_test_mode("tests\\errors\\network\\receive_size_negative.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=6, 
        col_end=10, 
        code="PSNI-2"
        ):
        return False

    return True

def test_errors_network_send_not_variable() -> bool:
    run_in_test_mode("tests\\errors\\network\\send_not_variable.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=6, 
        col_end=7, 
        code="NNV-1"
        ):
        return False

    return True