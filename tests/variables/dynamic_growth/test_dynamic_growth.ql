any empty1 = [];
empty1[2] = 42;
println(empty1[0]); // 0 
println(empty1[1]); // 0
println(empty1[2]); // 42
println(#empty1); // 3

num nums = [10];
nums[3] = 99;
println(nums[2]); // 0
println(nums[3]); // 99
println(#nums); // 4

any grid = [];
grid[0] = [];
grid[0][2] = 5;
grid[1] = [1, 2];
grid[1][3] = 7;
println(grid[0][2]); // 5
println(grid[0][0]); // 0
println(grid[1][3]); // 7
println(#grid); // 2

any empty2 = [];
println(empty2[1]); // should grow and print 0.0
println(#empty2); // 2

any empty3 = [];
empty3[5] = 10;
println(#empty3); // 6
println(empty3[0]); // 0.0
println(empty3[5]); // 10

any text_arr = ["a"];
text_arr[2] = "c";
println(text_arr[1]); // ""
println(text_arr[2]); // "c"

any empty4 = [];
println(empty4[2][1]); // 0.0
println(#empty4); // 3
