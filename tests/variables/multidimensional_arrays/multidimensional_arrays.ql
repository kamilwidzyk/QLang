// Comprehensive test for multidimensional arrays in QLang
// Tests NUM and OBS arrays of various dimensions

println("=== Testing 1D NUM Arrays ===");

// 1D array with initialization
num arr1d[5] = [10, 20, 30, 40, 50];
println("arr1d:", arr1d);
println("arr1d[0]:", arr1d[0]);
println("arr1d[4]:", arr1d[4]);
println("#arr1d:", #arr1d);

// 1D array without initialization (should be zeros)
num arr1d_empty[3];
println("arr1d_empty:", arr1d_empty);
println("arr1d_empty[2]:", arr1d_empty[2]);

println();
println("=== Testing 2D NUM Arrays ===");

// 2D array with initialization
num arr2d[2][3] = [
    [1, 2, 3],
    [4, 5, 6]
];
println("arr2d:", arr2d);
println("arr2d[0]:", arr2d[0]);
println("arr2d[1]:", arr2d[1]);
println("arr2d[0][1]:", arr2d[0][1]);
println("arr2d[1][2]:", arr2d[1][2]);
println("#arr2d:", #arr2d);

// 2D array without initialization
num arr2d_empty[2][2];
println("arr2d_empty:", arr2d_empty);

println();
println("=== Testing 3D NUM Arrays ===");

// 3D array with initialization
num arr3d[2][2][2] = [
    [
        [1, 2],
        [3, 4]
    ],
    [
        [5, 6],
        [7, 8]
    ]
];
println("arr3d:", arr3d);
println("arr3d[0]:", arr3d[0]);
println("arr3d[1][0]:", arr3d[1][0]);
println("arr3d[0][1][0]:", arr3d[0][1][0]);
println("arr3d[1][1][1]:", arr3d[1][1][1]);
println("#arr3d:", #arr3d);

// 3D array without initialization
num arr3d_empty[1][2][3];
println("arr3d_empty:", arr3d_empty);

println();
println("=== Testing OBS Arrays ===");

// OBS arrays (quantum observables)
obs obs1d[3];
obs1d = 5 >3> obs; // binary 101
println("obs1d[1]:", obs1d[1]);
println("#obs1d:", #obs1d);

println();
println("=== Testing Array Assignments ===");

// Test assignment to array elements
num test_assign[3] = [0, 0, 0];
println("Before assignment:", test_assign);
test_assign[1] = 99;
println("After test_assign[1] = 99:", test_assign);

// Test 2D assignment
num test_assign_2d[2][2] = [
    [0, 0],
    [0, 0]
];
println("Before 2D assignment:", test_assign_2d);
test_assign_2d[1][0] = 77;
println("After test_assign_2d[1][0] = 77:", test_assign_2d);

println();
println("=== Testing Array Operations ===");

// Test array in expressions
num calc_arr[3] = [1, 2, 3];
num result = calc_arr[0] + calc_arr[1] * calc_arr[2];
println("calc_arr[0] + calc_arr[1] * calc_arr[2] =", result);

// Test array in ternary
num ternary_arr[2] = [10, 20];
num ternary_result = ternary_arr[0] > 5 ? ternary_arr[0] : ternary_arr[1];
println("Ternary with array element:", ternary_result);

println();
println("=== Testing Large Arrays ===");

// Test larger arrays
num large_1d[10] = [0,1,2,3,4,5,6,7,8,9];
println("Large 1D array length:", #large_1d);
println("Large 1D array last element:", large_1d[9]);

num large_2d[3][4] = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12]
];
println("Large 2D array:", large_2d);
println("Large 2D array[2][3]:", large_2d[2][3]);

println();
println("=== All Array Tests Completed ===");