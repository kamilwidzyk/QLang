// and equal operator: left |= right
// this is the same as: left = left || right

num x = 0;
println(x |= 1); // 1, x is now 1
x |= 1; // x is now 1
println(x); // 1

x = 1;
println(x |= 1); // 1, x is now 1
x |= 1;  // x is now 1
println(x); // 1

println(x |= 0); // 1, x is now 1
x |= 0; // x is now 1
println(x); // 1

// expected output: 1\n1\n1\n1\n1\n1\n