from tests.test import *

def test_text_declaration() -> bool:
    run_in_test_mode("tests\\variables\\text\\declaration.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "\nabc\n"

    return place_log["global"] == expected_output

def test_text_assignment() -> bool:
    run_in_test_mode("tests\\variables\\text\\assignment.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "xyz\n123\n"

    return place_log["global"] == expected_output

def test_text_plus() -> bool:
    run_in_test_mode("tests\\variables\\text\\plus.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "hello world!\n"

    return place_log["global"] == expected_output

def test_text_minus() -> bool:
    run_in_test_mode("tests\\variables\\text\\minus.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "heo\nheo\n"

    return place_log["global"] == expected_output

def test_text_multi() -> bool:
    run_in_test_mode("tests\\variables\\text\\multi.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "aaa\nabcabc\nabcabcabc\n"

    return place_log["global"] == expected_output

def test_text_format() -> bool:
    run_in_test_mode("tests\\variables\\text\\format.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "test 42 value\ntest 42 value\n"

    return place_log["global"] == expected_output

def test_text_split() -> bool:
    run_in_test_mode("tests\\variables\\text\\split.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "['test', '42', 'value']\n"

    return place_log["global"] == expected_output

def test_text_index() -> bool:
    run_in_test_mode("tests\\variables\\text\\index.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "a\nab\nabc\n"

    return place_log["global"] == expected_output

def test_text_eq_not_eq() -> bool:
    run_in_test_mode("tests\\variables\\text\\eq_not_eq.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "T\nF\nF\nT\nT\nF\nF\nT\n"

    return place_log["global"] == expected_output

def test_text_cmp() -> bool:
    run_in_test_mode("tests\\variables\\text\\cmp.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = "T\nT\nT\nT\nT\nT\nF\nT\nT\nT\nT\nT\n"

    return place_log["global"] == expected_output