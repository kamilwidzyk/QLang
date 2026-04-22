// plus equal operator: expr += expr
// left is variable -> assign variable + right, return variable + right
// left is not variable -> return left + right, no assignment

// left is variable
num x = 10;
println(x); // 10
println(x += 15); // 25
println(x); // 25

x = 10;
println(x); // 10
x += 15; 
println(x); // 25

// left is not variable
println(10 += 15); // 25

// expected output: 10\n25\n25\n10\n25\n25\n