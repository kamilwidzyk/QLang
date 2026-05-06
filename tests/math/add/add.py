from tests.test import *



def test_addition() -> bool:
    run_in_test_mode("tests\\math\\add\\add.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])


    if place_log["global"] != "4\n4.0\n4.1\n0.0\n-0.10000000000000009\n":
        return False
    
    return True






