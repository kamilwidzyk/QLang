from tests.test import *


def test_nested_function():
    run_in_test_mode("tests\\function\\nested\\nested.ql")

    test_lines = extract_test_lines_from_log()
    if SYNTAX_ERRORS in test_lines:
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected = "inner\nouter\n15\nfrom if\n0\n1\n2\n"

    if place_log["global"] != expected:
        print("Expected: " + expected.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False

    return True
