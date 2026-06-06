from tests.test import *

def test_multiple_args_syntax() -> bool:
    run_in_test_mode("tests\\function\\definition\\multiple_args_syntax.ql")
    
    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False
        
    return True
