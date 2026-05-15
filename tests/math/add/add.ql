
// int + int = int
println(2 + 2); // 4

// float + int = float
println(2.5 + 2); // 4.5

// int + float = float
println(2 + 2.5); // 4.5

// float + float = float
println(2.5 + 2.5); // 5.0

// bool + bool -> bool gets converted to int
println(T + T); // 2
println(T + F); // 1
println(F + T); // 1
println(F + F); // 0


// bool + int
println(T + 5); // 6
println(F + 5); // 5

// int + bool
println(5 + T); // 6
println(5 + F); // 5

// bool + float
println(5.5 + T); // 6.5
println(5.5 + F); // 5.5

// float + bool
println(T + 5.5); // 6.5
println(F + 5.5); // 5.5




// expected output: 4\n4.5\n4.5\n5.0\n2\n1\n1\n0\n6\n5\n6\n5\n6.5\n5.5\n6.5\n5.5\n
