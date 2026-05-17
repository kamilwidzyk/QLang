place Przyklad1 {
    num x = 1;
    num y = 100;
    if(1) {
        num x = 2;
        if(1) {
            num x = 3;
            println(x);
            println(parent(x));
            println(parent(parent(x)));

            println(y);
            println(parent(y));
            println(parent(parent(y)));
        }
    }
}