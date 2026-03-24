obs someObs[4] = 5;
print(someObs);


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
    print("Podaj liczbę 1-10: ");
    input(repeatTimes, 1..10);
    println();

    print("Podałeś liczbę: ");
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

    print("Wynik w formacie BIN: ");
    println(result, BIN);

    if (result > 200) {
        println("Wynik jest większy niż 200!");
    } else {
        println("Wynik jest mniejszy lub równy 200.");
    }

    println();

    obs a[8] = 5;
    obs b[8] = 10;
    obs c[8] = 3;
    obs one = 1;
    obs zero = 0;

    print("a = ");
    println(a);
    print("b = ");
    println(b);
    print("c = ");
    println(c);

    println();
    print("a + b = ");
    println(a + b);

    println();
    print("a - b = ");
    println(a - b);

    println();
    print("!a = ");
    println(!a);
    print("!c = ");
    println(!c);

    println();
    print("a * b = ");
    println(a * b);

    println();
    print("a / b = ");
    println(a / b);
    print("b / a = ");
    println(b / a);

    println();
    print("b % a = ");
    println(b % a);
    print("a % c = ");
    println(a % c);

    println();
    print("a == a = ");
    println(a == a);
    print("a == b = ");
    println(a ==  b);
    
    println();
    print("a != b = ");
    println(a != b);
    print("a != a = ");
    println(a != a);

    println();
    print("one && one = ");
    println(one && one);
    print("one && zero = ");
    println(one && zero);
    print("zero && one = ");
    println(zero && one);
    print("zero && zero = ");
    println(zero && zero);

    println();
    print("one || one = ");
    println(one || one);
    print("one || zero = ");
    println(one || zero);
    print("zero || one = ");
    println(zero || one);
    print("zero || zero = ");
    println(zero || zero);

    println();
    print("T = ");
    println(T);
    print("F = ");
    println(F);

    println();
    print("a + b * c = ");
    println(a + b * c);
    print("a * b + c = ");
    println(a * b + c);
    print("(a + b) * c = ");
    println((a + b) * c);
    print("a + (b * c) = ");
    println(a + (b * c));









}