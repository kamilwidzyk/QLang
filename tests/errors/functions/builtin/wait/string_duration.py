from tests.test import *

def test_errors_functions_builtin_wait_string_duration() -> bool:
    run_in_test_mode("tests\\errors\\functions\\builtin\\wait\\string_duration.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=3, 
        line_end=3, 
        col_start=6, 
        col_end=11, 
        code="WDNN-1"
        ):
        return False

    return True

