from tests.test import *



def test_io_printf() -> bool:
    run_in_test_mode("tests\\io\\printf\\printf.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = 'x = 42, y = 3.14\nHello world\n'

    if place_log["global"] != expected_output:
        print("Expected: " + repr(expected_output))
        print("Got: " + repr(place_log["global"]))
        return False
    
    return True