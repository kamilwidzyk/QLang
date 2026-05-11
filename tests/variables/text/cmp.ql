text a = "apple";
text b = "banana";
text c = "apple";
text d = "Apple";

println(a < b); // T (apple < banana)
println(b > a); // T (banana > apple)
println(a <= c); // T (apple <= apple)
println(a <= b); // T (apple <= banana)
println(b >= a); // T (banana >= apple)
println(a >= c); // T (apple >= apple)
println(a < d); // F (apple > Apple)
println(d < a); // T (Apple < apple)
println("abc" < "abd"); // T
println("abc" > "abb"); // T
println("abc" <= "abc"); // T
println("abc" >= "abc"); // T

// Expected output:
// T
// T
// T
// T
// T
// T
// F
// T
// T
// T
// T
// T