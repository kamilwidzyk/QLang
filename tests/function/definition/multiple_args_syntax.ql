// Podstawowa definicja
function x(...nums){
    println("hello from x");
}

// Wywołania
x();
x(1, 2, 3);

// Ze spacją
function x2(... nums){}

// Z innymi argumentami
function x3(num y, ...nums) {}
function sum(num start, ...nums){}

// Zagnieżdżona
function y(){
    function x4(...nums){}
}

// Wewnątrz place
place P {
    function x5(...nums){}
}
