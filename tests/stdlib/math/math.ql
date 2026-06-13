<< "stdlib/math.ql" >>

println(abs(5.0)); // 5.0
println(abs(0.0 - 10.0)); // 10.0

println(minimum(3, 7)); // 3
println(minimum(10, 2)); // 2

println(maximum(3, 7)); // 7
println(maximum(10, 2)); // 10

println(maximum(minimum(10, 20), abs(0 - 50))); // max(10, 50) -> 50

num largest = 0;
for i from 1 to 6 {
    largest = maximum(largest, i);
}
println(largest); // 5

num arr[3];
arr[0] = 5;
arr[1] = 0 - 2;
arr[2] = 10;
println(abs(arr[1])); // 2
println(maximum(arr[0], arr[2])); // 10

println(minimum(0.5, 0.0 - 1.5)); // -1.5
println(maximum(0.0 - 5.5, 0.0 - 2.2)); // -2.2

println(abs((10 - 20) * 2)); // abs(-20) -> 20

println(minimum(42, 42)); // 42
println(maximum(42, 42)); // 42

num complex_res = maximum(abs(0 - 100), minimum(200, 50)); // max(100, 50) -> 100
println(complex_res); // 100

function custom_math_op(num x, num y) {
    return maximum(abs(x), abs(y));
}

println(custom_math_op(0.0 - 5.0, 3.0)); // 5.0
