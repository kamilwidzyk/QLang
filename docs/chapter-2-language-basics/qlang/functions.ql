function add(num a, num b) {
    return a + b;
}

function greet(text name = "World") {
    println("Hello, " + name + "!");
}

function power(num base, num exp) {
    return base ** exp;
}

greet();                              // Hello, World!
greet("Alice");                       // Hello, Alice!
println(add(3, 4));                   // 7
println(power(exp = 3, base = 2));    // 8
