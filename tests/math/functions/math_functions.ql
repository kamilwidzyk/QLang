// test cut
println(cut(3.14159)); // 3
println(cut(3.14159, 2)); // 3.14
println(cut(-3.14159)); // -3
println(cut(-3.14159, 2)); // -3.14

// test round
println(round(3.5)); // 4
println(round(3.4)); // 3
println(round(-3.5)); // -4
println(round(3.14159, 2)); // 3.14
println(round(3.14659, 2)); // 3.15

// test floor
println(floor(3.9)); // 3
println(floor(-3.1)); // -4
println(floor(3.146, 2)); // 3.14

// test ceil
println(ceil(3.1)); // 4
println(ceil(-3.9)); // -3
println(ceil(3.141, 2)); // 3.15

// test negativ
println(cut(123.456, -1)); // 120
println(round(125, -1)); // 130
println(floor(123, -1)); // 120
println(ceil(123, -1)); // 130
println(cut(0.0)); // 0
println(round(-0.0)); // 0
println(round(0.499999999999)); // 0
println(round(0.500000000001)); // 1
println(cut(999999999.999)); // 999999999
println(cut(999999999.999, -2)); // 999999900
