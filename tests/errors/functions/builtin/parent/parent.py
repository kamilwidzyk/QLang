from tests.test import *

def test_errors_function_builtin_parent_undefined_variable() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\parent\\undefined_variable.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=20, 
        col_end=21, 
        code="CFV-4"
        ):
        return False

    return True

def test_errors_function_builtin_parent_more_args() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\parent\\more_args.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=16, 
        code="TMA-3"
        ):
        return False

    return True

def test_errors_function_builtin_parent_named_arg() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\parent\\named_arg.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=1, 
        col_end=15, 
        code="KANS-2"
        ):
        return False

    return True


def test_errors_function_builtin_parent_named_arg2() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\parent\\named_arg2.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=8, 
        col_end=22, 
        code="KANS-2"
        ):
        return False

    return True

def test_errors_function_builtin_parent_invalid_val() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\parent\\invalid_val.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=2, 
        line_end=2, 
        col_start=8, 
        col_end=9, 
        code="BEV-2"
        ):
        return False

    return True

def test_errors_function_builtin_parent_too_much() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\parent\\too_much.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=19, 
        col_end=20, 
        code="NPS-1"
        ):
        return False

    return True