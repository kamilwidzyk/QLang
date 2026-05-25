from tests.test import *

def test_math_functions() -> bool:
    run_in_test_mode("tests\\math\\functions\\math_functions.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    expected_output = "3\n3.14\n-3\n-3.14\n4\n3\n-4\n3.14\n3.15\n3\n-4\n3.14\n4\n-3\n3.15\n120\n130\n120\n130\n0\n0\n0\n1\n999999999\n999999900\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True
