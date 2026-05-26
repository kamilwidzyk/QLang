
// a: Funkcja zagniezdzona wewnatrz innej funkcji
function outer() {
    function inner() {
        println("inner");
    }
    inner();
    println("outer");
}
outer();

// b: Funkcja zagniezdzona z dostepem do zmiennej zewnetrznej - closure
function make_adder(num x) {
    function adder(num y) {
        println(x + y);
    }
    adder(10);
}
make_adder(5);

// c: Funkcja zadeklarowana w bloku if
num flag = 1;
if(flag == 1) {
    function inside_if() {
        println("from if");
    }
    inside_if();
}

// d: Funkcja zadeklarowana w petli for
for i from 0 to 3 step 1 {
    function loop_func() {
        println(i);
    }
    loop_func();
}

// expected output: inner\nouter\n15\nfrom if\n0\n1\n2\n
