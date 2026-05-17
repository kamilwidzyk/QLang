

place systemA{
    function callMe(obs num[32]){
        print("Poziom: ");
        println(num);

        callMe(num + 1);
    }

    println("Nieskonczona rekurencja");
    callMe(0);
}


place systemB{
    function showNumber(obs num[32]){
        print("Iteracja: ");
        println(num);
    }

    println("Dluga petla");

    for i from 0 to 1000000000 step 1 {
        showNumber(i);
    }
}
