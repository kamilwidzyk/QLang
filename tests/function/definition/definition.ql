
function f1(){ // no arguments

}
println("F1");


function f2(num x){ // one argument

}
println("F2");


function f3(num x, num y){ // two arguments

}
println("F3");


function f4(num x, num y, num z){ // three arguments

}
println("F4");


function f5(num x[10]){ // one array argument

}
println("F5");


function f6(num x[10], num y){ // one array, one num

}
println("F6");


function f7(num x[10], num y[20]){ // two arrays

}
println("F7");

// expected output: F1\nF2\nF3\nF4\nF5\nF6\nF7\n