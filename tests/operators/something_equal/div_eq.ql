// div equal operator: expr /= expr
// left is variable -> assign variable / right, return variable / right

// left is variable
num x = 10;
println(x); // 10
println(x /= 2); // 5
println(x); // 5

x = 10;
println(x); // 10
x /= 2;
println(x); // 5

// expected output: 10\n5\n5\n10\n5\n