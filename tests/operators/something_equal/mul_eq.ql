// mul equal operator: expr *= expr
// left is variable -> assign variable * right, return variable * right

// left is variable
num x = 10;
println(x); // 10
println(x *= 2); // 20
println(x); // 20

x = 10;
println(x); // 10
x *= 2;
println(x); // 20

// expected output: 10\n20\n20\n10\n20\n