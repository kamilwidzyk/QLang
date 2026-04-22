// pre decrement: --expr
// decrement, then return value


println(--1); // 0
println(--0); // -1
println(--(-1)); // -2

num x = 2;
println(x); // 2
println(--x); // 1, x is now 1
println(x); // 1
println(--x); // 0, x is now 0
println(x); // 0

// expected output: 0\n-1\n-2\n2\n1\n1\n0\n0\n


