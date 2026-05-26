from tests.test import *

def test_variable_any() -> bool:
    run_in_test_mode("tests\\variables\\any\\any.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    expected_output = "123\ntext_test\n[1, 2, 3]\nassigned\n15\nhello world\n[10, 20, 30]\n20\n[[1, 2], [3, 4]]\n3\n[]\n50\nreturned_string\n7\nT\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True



