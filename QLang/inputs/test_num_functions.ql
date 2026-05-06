place TestNumFunctions {
    // TEST 1: funkcja zwracajaca num, parametry num

    function num dodaj(num a, num b) {
        return a + b;
    }

    function num odejmij(num a, num b) {
        return a - b;
    }

    function num pomnoz(num a, num b) {
        return a * b;
    }

    function num podziel(num a, num b) {
        return a / b;
    }

    println("TEST 1: podstawowe dzialania na parametrach num");
    num x = 10;
    num y = 4;

    print("dodaj(10, 4)    = "); println(dodaj(x, y));
    print("odejmij(10, 4)  = "); println(odejmij(x, y));
    print("pomnoz(10, 4)   = "); println(pomnoz(x, y));
    print("podziel(10, 4)  = "); println(podziel(x, y));

    // TEST 2: funkcja void z parametrem num

    function void wypisz_wynik(num wartosc) {
        print("  Wynik: ");
        println(wartosc);
    }

    function void wypisz_linie(num n) {
        for i from 0 to n {
            print("-");
        }
        println("");
    }

    println("");
    println("TEST 2: funkcja void z parametrem num");
    wypisz_linie(20);
    wypisz_wynik(dodaj(7, 13));
    wypisz_wynik(pomnoz(6, 6));
    wypisz_linie(20);

    // TEST 3: rekurencja z parametrem num

    function num silnia(num n) {
        if (n <= 1) {
            return 1;
        }
        return n * silnia(n - 1);
    }

    println("");
    println("TEST 3: silnia z parametrem num");
    for i from 0 to 8 {
        print("silnia(");
        print(i);
        print(") = ");
        println(silnia(i));
    }

    // TEST 4: przekazywanie wyniku funkcji do funkcji

    function num kwadrat(num n) {
        return n * n;
    }

    function num suma_kwadratow(num a, num b) {
        return kwadrat(a) + kwadrat(b);
    }

    println("");
    println("TEST 4: kompozycja funkcji");
    print("kwadrat(5)            = "); println(kwadrat(5));
    print("kwadrat(12)           = "); println(kwadrat(12));
    print("suma_kwadratow(3, 4)  = "); println(suma_kwadratow(3, 4));
    print("suma_kwadratow(5, 12) = "); println(suma_kwadratow(5, 12));

    // TEST 5: funkcja num z logiką warunkową

    function num max(num a, num b) {
        if (a > b) {
            return a;
        }
        return b;
    }

    function num min(num a, num b) {
        if (a < b) {
            return a;
        }
        return b;
    }

    function num abs_val(num n) {
        if (n < 0) {
            return n * -1;
        }
        return n;
    }

    println("");
    println("TEST 5: funkcje z logika warunkowa");
    print("max(7, 3)    = "); println(max(7, 3));
    print("max(3, 7)    = "); println(max(3, 7));
    print("min(7, 3)    = "); println(min(7, 3));
    print("abs_val(-5)  = "); println(abs_val(-5));
    print("abs_val(5)   = "); println(abs_val(5));

    // TEST 6: funkcja z petla wewnatrz, parametr num

    function num suma_do_n(num n) {
        num wynik = 0;
        for i from 1 to n {
            wynik = wynik + i;
        }
        return wynik;
    }

    function num potega(num podstawa, num wykladnik) {
        num wynik = 1;
        for i from 0 to wykladnik {
            wynik = wynik * podstawa;
        }
        return wynik;
    }

    println("");
    println("TEST 6: petla wewnatrz funkcji num");
    print("suma_do_n(10)    = "); println(suma_do_n(10));
    print("suma_do_n(100)   = "); println(suma_do_n(100));
    print("potega(2, 8)     = "); println(potega(2, 8));
    print("potega(3, 4)     = "); println(potega(3, 4));

    // TEST 7: literaly jako argumenty

    println("");
    println("TEST 7: literaly jako argumenty num");
    print("dodaj(100, 200)     = "); println(dodaj(100, 200));
    print("silnia(7)           = "); println(silnia(7));
    print("suma_kwadratow(8,6) = "); println(suma_kwadratow(8, 6));

    // TEST 8: wynik funkcji przypisany do zmiennej

    println("");
    println("TEST 8: wynik funkcji do zmiennej");
    num a = silnia(5);
    num b = potega(2, 10);
    num c = dodaj(a, b);
    print("silnia(5)                    = "); println(a);
    print("potega(2, 10)                = "); println(b);
    print("dodaj(silnia(5), 2^10)       = "); println(c);
}
