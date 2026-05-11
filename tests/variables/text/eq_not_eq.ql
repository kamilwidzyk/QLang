text x = "x";
text y = "y";

println(x == "x"); // T
println(x == y); // F
println(x != "x"); // F
println(x != y); // T

println("x" == "x"); // T
println("x" == "y"); // F
println("x" != "x"); // F
println("x" != "y"); // T

// expected output: T\nF\nF\nT\nT\nF\nF\nT\n