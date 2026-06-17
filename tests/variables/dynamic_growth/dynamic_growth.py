from tests.test import *

def test_dynamic_growth() -> bool:
    run_in_test_mode("tests\\variables\\dynamic_growth\\test_dynamic_growth.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    expected_output = "0.0\n0.0\n42\n3\n0.0\n99\n4\n5\n0.0\n7\n2\n0.0\n2\n6\n0.0\n10\n\nc\n0.0\n3\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True
