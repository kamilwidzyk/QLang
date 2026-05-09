
function f1(){ // no arguments
    println("F1");
}
f1(); // F1


function f2(num x){ // one argument
    print("F2 ");
    if(x > 10){
        println("x > 10");
    }else{
        println("x <= 10");
    }
}
f2(10); // F2 x <= 10


function f3(num x, num y){ // two arguments
    x = y;
    print("F3 x=");
    print(x);
    print(" y=");
    print(y);
    if(x > y){
        println(" x > y");
    }else{
        println(" x <= y");
    }
}
f3(5, 10); // F3 x=5 y=10 x <= y


// expected output: F1\nF2 x <= 10\nF3 x=5 y=10 x <= y\n
