any x = 123;
any y = "text_test";
any z[?] = [1, 2, 3];
any uninit;

println(x); // 123
println(y); // text_test
println(z); // [1, 2, 3]

uninit = "assigned";
println(uninit); // assigned

function test_any_func(any a, any b) {
    return a + b;
}

println(test_any_func(5, 10)); // 15
println(test_any_func("hello ", "world")); 

any sized_arr[3];
sized_arr = [10, 20, 30];
println(sized_arr);
println(sized_arr[1]);

any nested[?] = [[1, 2], [3, 4]];
println(nested);
println(nested[1][0]);

any empty_list[?] = [];
println(empty_list);

function strictly_typed(num x) {
    return x * 10;
}
any dynamically_typed_num = 5;
println(strictly_typed(dynamically_typed_num));

function return_any(any in_val) {
    return in_val;
}
println(return_any("returned_string"));
any ret_arr[?] = return_any([9, 8, 7]);
println(ret_arr[2]);

any b = T;
println(b);
