num y = 0;
if(T){
    num x = 0;
    println(x);
    println(parent(x)); // <- error here
}
-----------------------------------------
num y = 0;
if(T){
    num x = 0;
    println(x);
    println(^x); // <- error here
}