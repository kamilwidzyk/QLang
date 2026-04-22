// post increment: expr++
// return value, then increment(if variable)
// note: this does nothing on normal numbers

println(1++); // 1
println(0++); // 0
println(-1++); // -1

num x = 2;
println(x); // 2
println(x++); // 2, x is now 3
println(x); // 3
println(x++); // 3, x is now 4
println(x); // 4

// expected output: 1\n0\n-1\n2\n2\n3\n3\n4\n


