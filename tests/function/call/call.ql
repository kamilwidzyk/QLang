
function f1(){ // no arguments
    println("F1");
}
f1(); // F1


function f2(num x){ // one argument
    print("F2 x=");
    println(x);
}
f2(10); // F2 x=10


function f3(num x, num y){ // two arguments
    print("F3 x=");
    print(x);
    print(" y=");
    println(y);
}
f3(5, 10); // F3 x=5 y=10

function f4(num x, num y, num z){ // three arguments
    print("F4 x=");
    print(x);
    print(" y=");
    print(y);
    print(" z=");
    println(z);
} 
f4(5, 10, 15); // F4 x=5 y=10 z=15

function f5(num x){ // one arg, return +1
    return x + 1;
}
println(f5(9)); // 10

function f6(){
    println("F6");
    return;
    println("F6 Failed");
}


// expected output: F1\nF2 x=10\nF3 x=5 y=10\nF4 x=5 y=10 z=15\n10\nF6\n