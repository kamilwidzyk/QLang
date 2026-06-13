from tests.test import *

def test_errors_function_builtin_num_two_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\num\\two_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=9, 
        col_end=22, 
        code="TMA-2"
        ):
        return False

    return True

def test_errors_function_builtin_num_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\num\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=12, 
        code="KANS-1"
        ):
        return False

    return True

def test_errors_function_builtin_num_invalid_val() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\num\\invalid_val.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=11, 
        code="BEV-1"
        ):
        return False

    return True
