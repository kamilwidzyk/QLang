// Variable declarations
obs counter[8] = 0;
obs result[16];
num pi = 3.14159;
text greeting = "Hello!";
state q;
state reg[4];

// Array access
obs values[10];
values[0] = 1;
values[9] = 99;
obs len = #values;    // len == 10

// Arithmetic and format output
obs x[8] = 255;
println(x);         // 255
println(x, BIN);    // 11111111
println(x, HEX);    // FF

// String formatting
println("The answer is %d" % x);
