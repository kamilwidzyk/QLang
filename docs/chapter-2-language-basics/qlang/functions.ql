function add(obs a[8], obs b[8]) {
    return a + b;
}

function greet(text name = "World") {
    println("Hello, " + name + "!");
}

function power(obs base[8], obs exp[8]) {
    return base ** exp;
}

greet();                       // Hello, World!
greet(name = "Alice");         // Hello, Alice!
println(add(3, 4));            // 7
println(power(exp = 3, base = 2));  // 8
