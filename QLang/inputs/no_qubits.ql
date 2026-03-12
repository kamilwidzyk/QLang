place ClassicalSystem {
    function greetUser(obs count[8]) {
        println("--- Rozpoczynam powitanie ---");
        
        for i from 1 to count {
            print("Wiadomosc nr ");
            print(i);
            print(": ");
            println("Hello, QLang World!");
        }
        
        println("--- Koniec powitania ---");
    }

    obs repeatTimes[8];
    print("Podaj liczbe 1-10: ");
    intput(repeatTimes);
    println();

    print("Podales liczbe: ");
    println(repeatTimes);

    greetUser(repeatTimes);

    obs base[4] = 2;
    obs exp[4] = 8;
    obs result[10] = base ** exp;

    println();
    print("Obliczenie klasyczne (2^8): ");
    println(result);

    print("Wynik w formacie HEX: ");
    println(result, HEX);

    if (result > 200) {
        println("Wynik jest wiekszy niz 200!");
    } else {
        println("Wynik jest mniejszy lub rowny 200.");
    }
}