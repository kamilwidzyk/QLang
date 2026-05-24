from tests.test import *



def test_variable_obs() -> bool:
    run_in_test_mode("tests\\variables\\obs\\obs.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = "[A] FFT\n[B] TFT\n[C] FTF\n[DEF] FFFTTT\n[G] TTFFFFTTT\n7\n"

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True