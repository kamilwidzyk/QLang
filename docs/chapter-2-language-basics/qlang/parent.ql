num x = 1;
if (1) {
    num x = 2;
    if (1) {
        println(^^x);  // 1 - grandparent x
        ^x = 10;
        println(^x);   // 10 - parent x
    }
}