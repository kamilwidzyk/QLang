function a(num x, ...b){
    println("x=%d #b=%d" % [x, #b]);
    for i from 0 to #b {
        println("b[%d]=%d" % [i, b[i]]);
    }
}

a(5, 10, 15); // x=5 #b=2\nb[0]=10\nb[1]=15\n
a(3); // x=3 #b=0\n
a(7, 6, 9, 12); // x=7 #b=3\nb[0]=6\nb[1]=9\nb[2]=12\n

// expected output: x=5 #b=2\nb[0]=10\nb[1]=15\nx=3 #b=0\nx=7 #b=3\nb[0]=6\nb[1]=9\nb[2]=12\n