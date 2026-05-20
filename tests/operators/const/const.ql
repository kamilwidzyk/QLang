// Const declaration tests
const num a = 5;
println("%d" % a);

num x = 10;
const x;
println("%d" % x);

const num arr[2] = [7, 8];
println("%d" % arr[0]);
println("%d" % arr[1]);

// Attempting to modify const should fail at runtime
// a = 6;
// arr[0] = 9;

// expected output: 5\n7\n8\n
