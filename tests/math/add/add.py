from tests.test import *



def test_math_add() -> bool:
    run_in_test_mode("tests\\math\\add\\add.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = "4\n4.5\n4.5\n5.0\nT\nT\nT\nF\n6\n5\n6\n5\n6.5\n5.5\n6.5\n5.5\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True






