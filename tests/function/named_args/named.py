from tests.test import *



def test_function_named_args() -> bool:
    run_in_test_mode("tests\\function\\named_args\\named.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])
    
    expected_output = "x=5 y=10\nx=3 y=4\nx=7 y=6\nx=8 y=9\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True
