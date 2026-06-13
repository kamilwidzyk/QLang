from tests.test import *

def test_stdlib_math() -> bool:
    run_in_test_mode("tests\\stdlib\\math\\math.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    expected_output = "5.0\n10.0\n3\n2\n7\n10\n50\n5\n2\n10\n-1.5\n-2.2\n20\n42\n42\n100\n5.0\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True
