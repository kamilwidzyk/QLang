// pow equal operator: expr **= expr
// left is variable -> assign variable ** right, return variable ** right

// left is variable
num x = 10;
println(x); // 10
println(x **= 2); // 100
println(x); // 100

x = 10;
println(x); // 10
x **= 2;
println(x); // 100

// expected output: 10\n100\n100\n10\n100\n