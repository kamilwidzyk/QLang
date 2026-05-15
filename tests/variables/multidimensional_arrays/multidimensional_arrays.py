from tests.test import *

def test_multidimensional_arrays() -> bool:
    run_in_test_mode("tests\\variables\\multidimensional_arrays\\multidimensional_arrays.ql")

    test_lines = extract_test_lines_from_log()
    if(SYNTAX_ERRORS in test_lines):
        print("\t ! Syntax errors")
        return False

    place_log = read_place_files_as_dict()
    if place_log.get("global") is None:
        return False

    print(place_log["global"])

    expected_output = (
        "=== Testing 1D NUM Arrays ===\n"
        "arr1d: [10, 20, 30, 40, 50]\n"
        "arr1d[0]: 10\n"
        "arr1d[4]: 50\n"
        "#arr1d: 5\n"
        "arr1d_empty: [0.0, 0.0, 0.0]\n"
        "arr1d_empty[2]: 0.0\n"
        "\n"
        "=== Testing 2D NUM Arrays ===\n"
        "arr2d: [[1, 2, 3], [4, 5, 6]]\n"
        "arr2d[0]: [1, 2, 3]\n"
        "arr2d[1]: [4, 5, 6]\n"
        "arr2d[0][1]: 2\n"
        "arr2d[1][2]: 6\n"
        "#arr2d: 2\n"
        "arr2d_empty: [[0.0, 0.0], [0.0, 0.0]]\n"
        "\n"
        "=== Testing 3D NUM Arrays ===\n"
        "arr3d: [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]\n"
        "arr3d[0]: [[1, 2], [3, 4]]\n"
        "arr3d[1][0]: [5, 6]\n"
        "arr3d[0][1][0]: 3\n"
        "arr3d[1][1][1]: 8\n"
        "#arr3d: 2\n"
        "arr3d_empty: [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]\n"
        "\n"
        "=== Testing OBS Arrays ===\n"
        "obs1d[1]: F\n"
        "#obs1d: 3\n"
        "\n"
        "=== Testing Array Assignments ===\n"
        "Before assignment: [0, 0, 0]\n"
        "After test_assign[1] = 99: [0, 99, 0]\n"
        "Before 2D assignment: [[0, 0], [0, 0]]\n"
        "After test_assign_2d[1][0] = 77: [[0, 0], [77, 0]]\n"
        "\n"
        "=== Testing Array Operations ===\n"
        "calc_arr[0] + calc_arr[1] * calc_arr[2] = 7\n"
        "Ternary with array element: 10\n"
        "\n"
        "=== Testing Large Arrays ===\n"
        "Large 1D array length: 10\n"
        "Large 1D array last element: 9\n"
        "Large 2D array: [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]\n"
        "Large 2D array[2][3]: 12\n"
        "\n"
        "=== All Array Tests Completed ===\n"
    )

    if place_log["global"] != expected_output:
        print("Expected: " + expected_output.replace("\n", "\\n"))
        print("Got: " + place_log["global"].replace("\n", "\\n"))
        return False

    return True
