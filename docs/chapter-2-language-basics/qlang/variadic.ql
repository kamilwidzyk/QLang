function sum(num ...values) {
    num s = 0;
    for i from 0 to #values {
        s += values[i];
    }
    return s;
}

println(sum(1, 2, 3));         // 6
println(sum(10, 20, 30, 40));  // 100

// Regular parameters can precede the variadic one
function prefixed(num x, num ...rest) {
    println("x=" + x + " count=" + #rest);
}

prefixed(5, 10, 15);   // x=5 count=2
