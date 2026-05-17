place Przyklad2 {
    num x = 100;

    function foo(num n) {
        num x = n;

        if (n > 0) {
            foo(n - 1);
        }
        
        print(x);
        print(" ");
        println(parent(x));
        
        return 0;  
    }

    foo(6);
}