from tests.test import *



def test_control_iterate() -> bool:
    run_in_test_mode("tests\\control\\iterate\\iterate.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = "10\n20\n30\n40\n50\n0: 10\n1: 20\n2: 30\n3: 40\n4: 50\napple\nbanana\ncherry\ntext\n123\n[1, 'b']\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True