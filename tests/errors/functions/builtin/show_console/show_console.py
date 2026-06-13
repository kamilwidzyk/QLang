from tests.test import *

def test_errors_function_builtin_show_console_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\show_console\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=22, 
        code="TMA-8"
        ):
        return False

    return True

def test_errors_function_builtin_show_console_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\show_console\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=21, 
        code="KANS-8"
        ):
        return False

    return True

def test_errors_function_builtin_show_console_invalid_val() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\show_console\\invalid_val.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=16, 
        code="BEV-6"
        ):
        return False

    return True