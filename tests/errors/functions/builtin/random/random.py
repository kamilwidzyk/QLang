from tests.test import *

def test_errors_function_builtin_random_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\random\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=16, 
        code="TMA-5"
        ):
        return False

    return True

def test_errors_function_builtin_random_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\random\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=15, 
        code="KANS-5"
        ):
        return False

    return True