// post decrement: expr--
// return value, then decrement(if variable)
// note: this does nothing on normal numbers

println(1--); // 1
println(0--); // 0
println(-1--); // -1

num x = 2;
println(x); // 2
println(x--); // 2, x is now 1
println(x); // 1
println(x--); // 1, x is now 0
println(x); // 0

// expected output: 1\n0\n-1\n2\n2\n1\n1\n0\n


