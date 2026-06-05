from tests.test import *

def test_network_variables() -> bool:
    run_in_test_mode("tests\\quantum\\network_variables\\network_variables.ql")

    test_lines = extract_test_lines_from_log()
    if SYNTAX_ERRORS in test_lines:
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("Receiver") is None:
        return False

    expected_output = "Hello\n"

    if place_log["Receiver"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["Receiver"].replace("\n", "\\n"))
        return False

    return True
