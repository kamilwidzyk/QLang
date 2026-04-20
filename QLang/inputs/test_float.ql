place test_float {
    println("--- TEST ZMIENNYCH FLOAT ---");
    num pi = 3.1415;
    num promien = 2.01;
    num nauk = 1e-5;
    num a = 1.1;
    num b = a;
    print("Wartosc a: ");
    println(a);
    print("Wartosc b: ");
    println(b);
    println("Wartosc pi: ") ;
    println(pi);
    println("Promien: ");
    println(promien);
    println("Naukowa notacja: ");
    println(nauk);

    println("--- TEST DZIALAN ---");
    num odej = 10.5 - 53123.21413;
    print("Wynik odejmowania to: ");
    println(odej);
    num mnoz = 3.14 * 2.0;
    print("Wynik mnozenia to: ");
    println(mnoz);
    num dziel = 11.0 / 3.0;
    print("Wynik dzielenia to: ");
    println(dziel);
    num poteg = 2.0 ** 3.0;
    print("Wynik potegowania to: ");
    println(poteg);
    num odej2 = 5.0 - 2.5;
    print("Wynik odejmowania 2 to: ");
    println(odej2);

    num f1 = 0;
    num f2 = 0.0;
    num i;
    for i from 1 to 100 step 1 {
        println(i);
        f1 = f1 + 0.1;
        f2 = 10 / f1;
    }
    print("Wartosc f1: ");
    println(f1);
    print("Wartosc f2: ");
    println(f2);

    println(")--- ROZPOZNANIE TYPOW ---");
    num integ = 5;
    num flt = 3.14;
    num dwa = 2;
    num wynik1 = integ / flt;
    num wynik2 = integ / dwa;
    num wynik3 = flt / dwa;
    print("Wynik dzielenia inta przez float: ");
    println(wynik1);
    print("Wynik dzielenia inta przez inta: ");
    println(wynik2);
    print("Wynik dzielenia floata przez inta: ");
    println(wynik3);
}