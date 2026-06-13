from tests.test import *

def test_errors_function_builtin_packet_log_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\packet_log\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=20, 
        code="TMA-7"
        ):
        return False

    return True


def test_errors_function_builtin_packet_log_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\packet_log\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=19, 
        code="KANS-7"
        ):
        return False

    return True

def test_errors_function_builtin_packet_log_invalid_val() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\packet_log\\invalid_val.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=14, 
        code="BEV-5"
        ):
        return False

    return True