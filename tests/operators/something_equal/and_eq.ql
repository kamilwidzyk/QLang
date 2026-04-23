// and equal operator: left &= right
// this is the same as: left = left && right

num x = 0;
println(x &= 1); // 0, x is now 0
x &= 1; // x is now 0
println(x); // 0

x = 1;
println(x &= 1); // 1, x is now 1
x &= 1;  // x is now 1
println(x); // 1

println(x &= 0); // 0, x is now 0
x &= 0; // x is now 0
println(x); // 0

// expected output: 0\n0\n1\n1\n0\n0\n