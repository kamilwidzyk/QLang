place systemA{
    function callMe(num x){
        print("Poziom: ");
        println(x);

        callMe(x + 1);
    }

    println("Nieskonczona rekurencja");
    callMe(0);
}


place systemB{
    function showNumber(num x){
        print("Iteracja: ");
        println(x);
    }

    println("Dluga petla");

    for i from 0 to 1000000000 {
        showNumber(i);
    }
}
