from tests.test import *


def test_errors_variable_non_existing() -> bool:
    run_in_test_mode("tests\\errors\\variables\\missing_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=1, 
        col_start=9, 
        col_end=25, 
        code="CFV-3"
        ):
        return False

    return True

def test_errors_variable_non_existing2() -> bool:
    run_in_test_mode("tests\\errors\\variables\\missing_var2.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=8, 
        line_end=8, 
        col_start=9, 
        col_end=11, 
        code="CFV-3"
        ):
        return False

    return True

def test_errors_variable_list_index_not_int() -> bool:
    run_in_test_mode("tests\\errors\\variables\\list_index_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=22, 
        col_end=35, 
        code="INI-4"
        ):
        return False

    return True

def test_errors_variable_list_index_not_int_var() -> bool:
    run_in_test_mode("tests\\errors\\variables\\list_index_not_int_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=22, 
        col_end=34, 
        code="INI-4"
        ):
        return False

    return True

def test_errors_variable_range_index_start_not_int() -> bool:
    run_in_test_mode("tests\\errors\\variables\\range_index_start_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=23, 
        col_end=26, 
        code="INI-2"
        ):
        return False

    return True

def test_errors_variable_range_index_start_not_int_var() -> bool:
    run_in_test_mode("tests\\errors\\variables\\range_index_start_not_int_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=23, 
        col_end=34, 
        code="INI-2"
        ):
        return False

    return True

def test_errors_variable_range_index_end_not_int() -> bool:
    run_in_test_mode("tests\\errors\\variables\\range_index_end_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=26, 
        col_end=29, 
        code="INI-3"
        ):
        return False

    return True

def test_errors_variable_range_index_end_not_int_var() -> bool:
    run_in_test_mode("tests\\errors\\variables\\range_index_end_not_int_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=26, 
        col_end=35, 
        code="INI-3"
        ):
        return False

    return True

def test_errors_variable_simple_index_not_int() -> bool:
    run_in_test_mode("tests\\errors\\variables\\simple_index_not_int.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=4, 
        line_end=4, 
        col_start=22, 
        col_end=27, 
        code="INI-5"
        ):
        return False

    return True

def test_errors_variable_simple_index_not_int_var() -> bool:
    run_in_test_mode("tests\\errors\\variables\\simple_index_not_int_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=5, 
        line_end=5, 
        col_start=22, 
        col_end=35, 
        code="INI-5"
        ):
        return False

    return True

def test_errors_variable_redefinition() -> bool:
    run_in_test_mode("tests\\errors\\variables\\redefinition.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=5, 
        col_end=6, 
        code="VR-1"
        ):
        return False

    return True

def test_errors_variable_out_of_range() -> bool:
    run_in_test_mode("tests\\errors\\variables\\out_of_range.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=-1, 
        line_end=-1, 
        col_start=-1, 
        col_end=-1, 
        code="IOR-1"
        ):
        return False

    return True

def test_errors_variable_shape_mismatch() -> bool:
    run_in_test_mode("tests\\errors\\variables\\shape_mismatch.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=-1, 
        line_end=-1, 
        col_start=-1, 
        col_end=-1, 
        code="SM-1"
        ):
        return False

    return True