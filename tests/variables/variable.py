from tests.test import *


def test_variable_non_existing() -> bool:
    run_in_test_mode("tests\\variables\\missing_var.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(2, 2, 8, 24, "CFV-3"):
        print("Expected runtime missing-variable error not found in test log")
        return False

    return True