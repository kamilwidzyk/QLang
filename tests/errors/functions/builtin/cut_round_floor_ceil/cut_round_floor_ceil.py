from tests.test import *

def test_errors_function_builtin_cut_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\cut_round_floor_ceil\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=13, 
        code="TMA-9"
        ):
        return False

    return True

def test_errors_function_builtin_cut_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\cut_round_floor_ceil\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=12, 
        code="KANS-9"
        ):
        return False

    return True

def test_errors_function_builtin_cut_invalid_first() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\cut_round_floor_ceil\\invalid_first.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=14, 
        code="BEV-7"
        ):
        return False

    return True

def test_errors_function_builtin_cut_invalid_second() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\cut_round_floor_ceil\\invalid_second.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=16, 
        code="BEV-8"
        ):
        return False

    return True