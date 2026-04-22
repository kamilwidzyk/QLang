// assignment operator: expr '=' expr
// left is variable: set left value to right, return right
// left is not variable: return right

// left is variable
num x = 10;
println(x); // 10
println(x = 15); // 15
println(x); // 15

// left is not variable
println(10 = 15); // 15

// expected output: 10\n15\n15\n15\n
