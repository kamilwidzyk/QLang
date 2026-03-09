// 1. Inicjalizacja
obs startState;
print("Podaj początkową wartość: ");
input(startState, BIN);

state data; // domyślnie 0
if(startState == 1){
    not data; // po odwróceniu 1
}

// 2. Kodowanie 
state ancilla[2]; // qubity pomocnicze
entangle data -> ancilla[0];
entangle data -> ancilla[1];

// 3. Symulacja błędu/pozostawienie wartości
obs makeError;
print("Wpisz 1 jeśli zasymulować błąd: ");
input(makeError, BIN);
if(makeError == 1){
    not data; // symulacja błędu
}

// 4. Detekcja błędu
state syn[2];
entangle data -> syn[0];
entangle ancilla[0] -> syn[0];

entangle ancilla[0] -> syn[1];
entangle ancilla[1] -> syn[1];

obs m[2] = measure syn;

// 5. Korekcja ewentualnego błędu
if(m == 0b10){
    not data;
}
if(m == 0b11){
    not ancilla[0];
}
if(m == 0b01){
    not ancilla[1];
}

print("Syndrom błędu: ");
println(m, BIN);
debug(data); // stan powinien być taki sam jak na początku