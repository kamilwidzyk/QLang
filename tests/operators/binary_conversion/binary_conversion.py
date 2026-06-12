from tests.test import *


def test_binary_conversion() -> bool:
    run_in_test_mode("tests\\operators\\binary_conversion\\binary_conversion.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    expected_output = "13\n13\n[1, 0, 1, 1]\n[0, 0, 0, 0]\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False

    return True
