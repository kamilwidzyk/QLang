num a = 5;
num b = a.0;
println(b); // 5.0

num c = 10;
println(c.0); // 10.0

println(15.0); // 15.0 (for comparison)

// Edge cases
println((2+3).0); // 5.0

// Function return cast
function get_val() {
    return 7;
}
println(get_val().0); // 7.0

// In a loop
num sum = 0.0;
for i from 1 to 4 {
    sum += i.0;
}
println(sum); // 6.0

// Array cast
num arr1d[3] = [10, 20, 30];
println(arr1d[1].0); // 20.0

// List cast
any my_list[?] = [4, 5, 6];
println(my_list[2].0); // 6.0

// Lexer edge cases
println(5.05);     // 5.05
println(5.05.0);   // 5.05
println(100.0);    // 100.0
