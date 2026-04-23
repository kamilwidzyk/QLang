// mod equal operator: expr %= expr
// left is variable -> assign variable % right, return variable % right

// left is variable
num x = 10;
println(x); // 10
println(x %= 2); // 0
println(x); // 0

x = 10;
println(x); // 10
x %= 2;
println(x); // 0


// expected output: 10\n0\n0\n10\n0\n