function test_empty(...args) {
    println(#args);
}
test_empty();

function test_single(...args) {
    println(#args);
    println(args[0]);
}
test_single(42);

function test_multi_num(...args) {
    println(#args);
    println(args[0] + args[1]);
}
test_multi_num(10, 20);

function test_mixed(...args) {
    println(#args);
    println(args[0]);
    println(args[1]);
    println(args[2]);
}
test_mixed(1, "text", T);

function test_with_normal(num a, text b, ...args) {
    println(a);
    println(b);
    println(#args);
    if (#args > 0) {
        println(args[0]);
    }
}
test_with_normal(100, "hello");
test_with_normal(100, "hello", 200, "world");
