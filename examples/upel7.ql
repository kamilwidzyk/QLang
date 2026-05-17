place Przyklad7 {
    function foo1(num a) {
        print("foo1:");
        println(a);
        
        if (a > 0) {
            foo2(a - 1);
        }
        return 0;
    }

    function foo2(num a) {
        print("foo2:");
        println(a);
        
        if (a > 0) {
            foo1(a - 2);
        }
        return 1;
    }

    foo1(10);
}