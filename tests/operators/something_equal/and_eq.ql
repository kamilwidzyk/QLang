// and equal operator: left &= right
// this is the same as: left = left && right

num x = 0;
println(x &= 1); // F, x is now 0
x &= 1; // x is now 0
println(x); // 0

x = 1;
println(x &= 1); // T, x is now 1
x &= 1;  // x is now 1
println(x); // 1

println(x &= 0); // F, x is now 0
x &= 0; // x is now 0
println(x); // 0

// expected output: F\n0\nT\n1\nF\n0\n