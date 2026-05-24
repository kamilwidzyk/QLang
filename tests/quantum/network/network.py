from tests.test import *


def test_quantum_network() -> bool:
    run_in_test_mode("tests\\quantum\\network\\network.ql")

    test_lines = extract_test_lines_from_log()
    if SYNTAX_ERRORS in test_lines:
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("Bob") is None:
        return False

    print(place_log["Bob"])

    expected_output = (
        "[state/from+named] T\n"
        "[obs/named-only] T\n"
        "[num-list/from+named] [7, 8, 9]\n"
        "[num/from+named] 42\n"
        "[text/named-only] hello network\n"
        "[text/from-only] broadcast\n"
    )

    if place_log["Bob"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["Bob"].replace("\n", "\\n"))
        return False

    return True

def test_quantum_network_available() -> bool:
    run_in_test_mode("tests\\quantum\\network\\available.ql")

    test_lines = extract_test_lines_from_log()
    if SYNTAX_ERRORS in test_lines:
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("Bob") is None:
        return False

    print(place_log["Bob"])

    expected_output = "[0, 6, 12, 5, 11]\n"

    if place_log["Bob"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["Bob"].replace("\n", "\\n"))
        return False

    return True