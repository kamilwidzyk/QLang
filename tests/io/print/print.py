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

    expected_output = (r"""This is a string
This is a string + a number: 42
This is a string + a list: [1, 2, 3]
This is a string + a list of strings: ["a", "b", "c"]
42 is a number + a string
[1, 2, 3] is a list + a string
["a", "b", "c"] is a list of strings + a string
This is a string concatenated with another string
This is a string concatenated with a list: [1, 2, 3]
This is a string and a mixed list: [1, "two", 3.0]
This is a string and a nested list: [1, [2, 3], 4]
This is a string and a nested list of strings: ["a", ["b", "c"], "d"]
This is a string ["a", "b", "c"] concatenated with a list and another string
The value of x is: 10
The value of y is: 3.14
The value of a is: 1
The value of b is: [F, F, F, T, F]
The value of s is: Hello, World!
The value of z is: [1, 2, 3, 4.0]
The value of nested_list is: [1, [2, 3], 4]
The value of bits is: [T, T, F, T, T, T, T, F, F, F]
""")

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False
    
    return True






