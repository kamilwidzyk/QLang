// reset operator: restores the variable to its initial or default value
num x = 5;
println(reset x);
println(x);

text s = "foo";
println(reset s);
println(s);

num arr[2][2] = [[1,2],[3,4]];
reset arr;
println(arr[0][0]);
println(arr[1][1]);

// expected output: 5\n5\nfoo\nfoo\n1\n4\n