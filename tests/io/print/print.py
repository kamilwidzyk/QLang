from tests.test import *



def test_io_print() -> bool:
    run_in_test_mode("tests\\io\\print\\print.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False
    
    print(place_log["global"])

    expected_output = (
        "This is a string\n"
        "This is a string + a number: 42\n"
        "This is a string + a list: [1, 2, 3]\n"
        "This is a string + a list of strings: [a, b, c]\n"
        "42 is a number + a string\n"
        "[1, 2, 3] is a list + a string\n"
        "[a, b, c] is a list of strings + a string\n"
        "This is a string concatenated with another string\n"
        "This is a string concatenated with a list: [1, 2, 3]\n"
        "This is a string and a mixed list: [1, two, 3.0]\n"
        "This is a string and a nested list: [1, [2, 3], 4]\n"
        "This is a string and a nested list of strings: [a, [b, c], d]\n"
        "This is a string [a, b, c] concatenated with a list and another string\n"
        "The value of x is: 10\n"
        "The value of y is: 3.14\n"
        "The value of a is: T\n"
        "The value of b is: 8\n"
        "The value of s is: Hello, World!\n"
        "The value of z is: [1, 2, 3, 4.0]\n"
    )

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True






