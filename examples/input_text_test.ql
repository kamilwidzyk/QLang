place TextSystem {
    println("--- Test modulu Input(text) ---");

    text t;
    println("Podaj slowo (dowolna dlugosc):");
    input(t);
    print("Wpisales: ");
    println(t);

    println("Test modulu Input(text) z ograniczeniami formatu");
    text password;
    println("Podaj haslo (tylko 4 do 8 znakow): ");
    input(password, 4..8);
    print("Poprawne haslo -> Twoje haslo to: ");
    println(password);

    println("Koniec");
}


