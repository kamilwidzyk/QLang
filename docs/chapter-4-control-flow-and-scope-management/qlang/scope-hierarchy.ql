num x = 1;
if (1) {
    num x = 2;
    if (1) {
        println("%d" % ^x);   // 2  - reads parent x
        ^x = 7;
        println("%d" % ^x);   // 7  - assigns to parent x
        (^x)++;
        println("%d" % ^x);   // 8
        ^x += 3;
        println("%d" % ^x);   // 11
        println("%d" % ^^x);  // 1  - reads grandparent x
    }
}