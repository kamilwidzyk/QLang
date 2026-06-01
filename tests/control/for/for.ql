// 'from' is inclusive
// 'to' is exclusive

// for counting up
println("FOR1");
for i from 0 to 5 { // '0 1 2 3 4 '
    print(i);
    print(" ");
} 
println();

// for counting down
println("FOR2");
for i from 5 to 0 step -1 { // '5 4 3 2 1 '
    print(i);
    print(" ");
} 
println();

num a = 5;
num b = 10;
num c = 2;

// for counting from 'a' to 'b'
println("FOR3");
for i from a to b { // '5 6 7 8 9 '
    print(i);
    print(" ");
} 
println();

// for counting from 'a' to 'b' with step 'c'
println("FOR4");
for i from a to b step c { // '5 7 9 '
    print(i);
    print(" ");
}
println();

// for counting up, counter changes inside
println("FOR5");
for i from 0 to 10 { // '0 1 3 7 '
    print(i);
    print(" ");
    i += i % 2;
}
println();

// for counting up, end value decreases
println("FOR6");
for i from a to b { // '5 6 7 '
    print(i);
    print(" ");
    b--;
}
println();
b = 10;

// for counting down, end value decreases, counter decreases
println("FOR7");
for i from b to a { // '10 8 6 4 2 '
    print(i);
    print(" ");
    a--;
    i--;
}
println();
a = 5;

// for counting up, step has 'i' in it (variable step)
println("FOR8");
for i from 0 to 20 step ((i % 5) + 1) { // '0 1 3 7 10 11 13 17 '
    print(i);
    print(" ");
}
println();

// for counting up, variable end
println("FOR9");
num x = 5;
for i from 0 to (-0.1 * i**2 + 0.1 * i + x) { // '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 '
    print(i);
    print(" ");
    x += 2;
}
println();

// for with function and variable declaration inside
println("FOR10");
for i from 0 to 3 {

    function increase_x(){
        x += 2;
    }

    num x = 10;

    increase_x();

    println("%d %d" % [i, x]);
}
// FOR10\n0 12\n1 12\n2 12\n