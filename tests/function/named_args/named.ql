function a(num x, num y){
    println("x=%d y=%d", x, y);
}
// invalid call: a(named, standard) - named arguments must come after standard ones
a(5, 10); // x=5 y=10
a(3, y=4); // x=3 y=4
a(y=6, x=7); // x=7 y=6
a(x=8, y=9); // x=8 y=9

// expected output: x=5 y=10\nx=3 y=4\nx=7 y=6\nx=8 y=9\n
