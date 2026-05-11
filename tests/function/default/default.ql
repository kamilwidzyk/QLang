function a(num x, num y = 20){
    println("x=%d y=%d", x, y);
}

a(5); // x=5 y=20
a(3, 4); // x=3 y=4
a(7, y=6); // x=7 y=6
a(x=8); // x=8 y=20
// expected output: x=5 y=20\nx=3 y=4\nx=7 y=6\nx=8 y=20\n