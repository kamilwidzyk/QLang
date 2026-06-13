from tests.test import *

def test_errors_function_args_named_repeated() -> bool:
    run_in_test_mode("tests\\errors\\functions\\args\\named_repeated.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=7, 
        line_end=7, 
        col_start=22, 
        col_end=29, 
        code="RKA-1"
        ):
        return False

    return True

def test_errors_function_args_missing_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\args\\missing_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=7, 
        line_end=7, 
        col_start=1, 
        col_end=7, 
        code="MA-1"
        ):
        return False

    return True

def test_errors_function_args_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\args\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=7, 
        line_end=7, 
        col_start=1, 
        col_end=15, 
        code="TMA-1"
        ):
        return False

    return True

def test_errors_function_unknown_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\args\\unknown_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=8, 
        line_end=8, 
        col_start=1, 
        col_end=30, 
        code="UA-1"
        ):
        return False

    return True

def test_errors_function_wrong_type() -> bool:
    run_in_test_mode("tests\\errors\\functions\\args\\wrong_type.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=8, 
        line_end=8, 
        col_start=1, 
        col_end=23, 
        code="IT-1"
        ):
        return False

    return True