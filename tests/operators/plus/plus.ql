// operator plus: '+' expr
//

println(+0); // 0
println(+1); // 1
println(+(1)); // 1
println(+(2)); // 2
println(+(+2)); // 2
println(+(+(2))); // 2
println(+(+(+2))); // 2

// expected output: 0\n1\n1\n2\n2\n2\n2\n
