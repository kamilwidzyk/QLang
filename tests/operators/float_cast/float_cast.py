from tests.test import *

def test_operator_float_cast() -> bool:
    run_in_test_mode("tests\\operators\\float_cast\\float_cast.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    expected_output = "5.0\n10.0\n15.0\n5.0\n7.0\n6.0\n20.0\n6.0\n5.05\n5.05\n100.0\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True
