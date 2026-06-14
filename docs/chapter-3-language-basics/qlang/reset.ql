// reset scalar
num x = 5;
x = 99;
reset x;
println(x);  // 5

// reset text
text s = "hello";
s = "world";
reset s;
println(s);  // hello

// reset array
num arr[2] = [1, 2];
arr[0] = 99;
reset arr;
println(arr[0]);  // 1