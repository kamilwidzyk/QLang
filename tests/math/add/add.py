from tests.test import *



def test_addition() -> bool:
    run_in_test_mode("tests\\math\\add.ql")

    test_lines = extract_test_lines_from_log()

    place_log = read_place_files_as_dict()


    if place_log.get("global") is None:
        return False
    
    if place_log["global"] != "4\n6\n":
        return False
    
    return True






