// Tests for '^' parent operator

num x = 1;
if(1){
    num x = 2;
    if(1){
        println("%d" % ^x); // 2
        ^x = 7;
        println("%d" % ^x); // 7
        (^x)++;
        println("%d" % ^x); // 8
        --(^x);
        println("%d" % ^x); // 7
        ^x += 3;
        println("%d" % ^x); // 10
        ^x *= 2;
        println("%d" % ^x); // 20
        println("%d" % ^^x); // 1
    }
}

num arr[2] = [10, 20];
if(1){
    if(1){
        println("%d" % ^^arr[0]); // 10
        println("%d" % ^^arr[1]); // 20
    }
}

// expected output: 2\n7\n8\n7\n10\n20\n1\n10\n20\n
