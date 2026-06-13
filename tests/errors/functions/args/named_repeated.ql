// Call function with repeated named args
function foo(num arg1, num arg2){
    println(arg1);
    println(arg2);
}

foo(arg1=5, arg2=10, arg1=15); // RKA-1 line 7..7 col 22..29