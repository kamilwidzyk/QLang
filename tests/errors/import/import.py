from tests.test import *


def test_errors_import_place() -> bool:
    run_in_test_mode("tests\\errors\\import\\place.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    if not print_error_entry(
        line_start=1, 
        line_end=3, 
        col_start=1, 
        col_end=2, 
        code="PDNA-1"
        ):
        return False

    return True