from tests.test import *
import time

def test_wait_statement() -> bool:
    start_time = time.time()
    
    run_in_test_mode("tests\\control_flow\\wait\\wait.ql")
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # 500ms + 1s + 100ms = 1.6s
    # In python it should take at least 1.6s
    place_log = read_place_files_as_dict()
    if elapsed < 1.5:
        print(f"\t ! Execution took too little time: {elapsed}s")
        print(place_log["global"])
        return False
    
    test_lines = extract_test_lines_from_log()
    if SYNTAX_ERRORS in test_lines:
        print("\t ! Syntax errors")
        return False
        
    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
        
    expected_output = "Start\nWaited 500ms\nWaited 1s\nWaited 0.1s\n"
    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
        
    return True
