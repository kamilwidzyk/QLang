
// int - int = int
println(5 - 3); // 2

// float - int = float
println(2.5 - 2); // 0.5

// int - float = float
println(3 - 2.5); // 0.5

// float - float = float
println(1.2 - 0.7); // 0.5

// bool - bool
println(T - T); // 0
println(T - F); // 1
println(F - T); // -1
println(F - F); // 0

// bool - int
println(T - 5); // -4
println(F - 5); // -5

// int - bool
println(5 - T); // 4
println(5 - F); // 5

// bool - float
println(T - 5.5); // -4.5
println(F - 5.5); // -5.5

// float - bool
println(5.5 - T); // 4.5
println(5.5 - F); // 5.5





// expected output: 2\n0.5\n0.5\n0.5\n0\n1\n-1\n0\n-4\n-5\n4\n5\n-4.5\n-5.5\n4.5\n5.5\n
