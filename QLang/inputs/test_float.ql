place test_float {
    println("--- TEST ZMIENNYCH FLOAT ---");
    num pi = 3.1415;
    num promien = 2.01;
    num nauk = 1e-5;
    println("Wartosc pi: ");
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
}