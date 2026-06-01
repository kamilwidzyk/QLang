function add(num a, num b) {
    return a + b;
}

function greet(text name = "World") {
    println("Hello, " + name + "!");
}

function power(num base, num exp) {
    return base ** exp;
}

// any parameter accepts any type
function print_value(any x) {
    println(x);
}

greet();                              // Hello, World!
greet("Alice");                       // Hello, Alice!
println(add(3, 4));                   // 7
println(power(exp = 3, base = 2));    // 8
print_value(42);                      // 42
print_value("hello");                 // hello
