from tests.test import *


def test_random_seed():
    run_in_test_mode("tests\\random\\random.ql")

    test_lines = extract_test_lines_from_log()
    if SYNTAX_ERRORS in test_lines:
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    expected_output = "0.8444218515250481\n0.7579544029403025\n1.0\n1.2589167502929635\n2.0225494427372173\n0\n"
    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False

    return True

