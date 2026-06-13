from tests.test import *

def test_errors_operators_binary_unsupported_type() -> bool:
    run_in_test_mode("tests\\errors\\operators\\binary\\unsupported_type.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=18, 
        col_end=22, 
        code="UCT-1"
        ):
        return False

    return True

def test_errors_operators_binary_list_of_twos() -> bool:
    run_in_test_mode("tests\\errors\\operators\\binary\\list_of_twos.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=9, 
        col_end=28, 
        code="ONS-7"
        ):
        return False

    return True

def test_errors_operators_binary_string_val() -> bool:
    run_in_test_mode("tests\\errors\\operators\\binary\\string_val.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=9, 
        col_end=21, 
        code="ONS-4"
        ):
        return False

    return True


def test_errors_operators_binary_bit_not_int() -> bool:
    run_in_test_mode("tests\\errors\\operators\\binary\\bit_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=9, 
        col_end=27, 
        code="ONS-5"
        ):
        return False

    return True

def test_errors_operators_binary_source_not_int() -> bool:
    run_in_test_mode("tests\\errors\\operators\\binary\\source_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=12, 
        col_end=26, 
        code="ONS-8"
        ):
        return False

    return True