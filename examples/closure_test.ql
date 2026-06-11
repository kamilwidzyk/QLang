num x = 10;

function foo(){
    x++;
}

if(1){
    num x = 20;
    foo();
    println(x); // 20
    println(^x); // 11
}

