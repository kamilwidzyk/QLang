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

