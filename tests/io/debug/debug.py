from tests.test import *

def test_debug() -> bool:
    run_in_test_mode("tests\\io\\debug\\debug.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    # This function is for debugging, format may change
    # Do not check anything
    
    return True