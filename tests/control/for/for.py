from tests.test import *



def test_control_for() -> bool:
    run_in_test_mode("tests\\control\\for\\for.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = \
        "FOR1\n" \
        "0 1 2 3 4 \n" \
        "FOR2\n" \
        "5 4 3 2 1 \n" \
        "FOR3\n" \
        "5 6 7 8 9 \n" \
        "FOR4\n" \
        "5 7 9 \n" \
        "FOR5\n" \
        "0 1 3 7 \n" \
        "FOR6\n" \
        "5 6 7 \n" \
        "FOR7\n" \
        "10 8 6 4 2 \n" \
        "FOR8\n" \
        "0 1 3 7 10 11 13 17 \n" \
        "FOR9\n" \
        "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 \n" \
        "FOR10\n" \
        "0 12\n1 12\n2 12\n"
    
    

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True






