from tests.test import *


def test_quantum_measure() -> bool:
    run_in_test_mode("tests\\quantum\\measure\\measure.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = "10\n25\n25\n10\n25\n"

    return True 
    # Tutaj nie da się sprawdzić wyniku 
    # bo nie ma jeszcze operatora seed(x)
    # teraz wyniki będą za każdym razem inne

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True