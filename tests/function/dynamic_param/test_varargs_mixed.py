from tests.test import *

def test_varargs_mixed() -> bool:
    run_in_test_mode("tests\\function\\dynamic_param\\test_varargs_mixed.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    expected_output = "0\n1\n42\n2\n30\n3\n1\ntext\nT\n100\nhello\n0\n100\nhello\n2\n200\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True
