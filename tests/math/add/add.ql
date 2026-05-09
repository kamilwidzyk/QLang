
// int + int = int
println(2 + 2);

// float + int = float
println(2.5 + 2);

// int + float = float
println(2 + 2.5);

// float + float = float
println(2.5 + 2.5);

// bool + bool
println(T + T); // T
println(T + F); // T
println(F + T); // T
println(F + F); // F

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




// expected output: 4\n4.5\n4.5\n5.0\nT\nT\nT\nF\n6\n5\n6\n5\n6.5\n5.5\n6.5\n5.5\n
