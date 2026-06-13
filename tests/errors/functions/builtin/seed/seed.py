from tests.test import *

def test_errors_function_builtin_seed_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\seed\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=14, 
        code="TMA-4"
        ):
        return False

    return True


def test_errors_function_builtin_seed_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\seed\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=13, 
        code="KANS-4"
        ):
        return False

    return True

def test_errors_function_builtin_seed_invalid_val() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\seed\\invalid_val.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=11, 
        code="BEV-3"
        ):
        return False

    return True