num indexes[?] = [0, 3, 5, 7];
text str = "abcdefghij";
//          0123456789

text literal_result = str[[1, 2, 3]];
println(literal_result); // bcd

text variable_result = str[indexes];
println(variable_result); // adfh