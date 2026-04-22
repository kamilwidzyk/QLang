// minus equal operator: expr -= expr
// left is variable -> assign variable - right, return variable - right
// left is not variable -> return left - right, no assignment

// left is variable
num x = 10;
println(x); // 10
println(x -= 15); // -5
println(x); // -5

x = 10;
println(x); // 10
x -= 15;
println(x); // -5

// left is not variable
println(10 -= 15); // -5



// expected output: 10\n-5\n-5\n10\n-5\n-5\n