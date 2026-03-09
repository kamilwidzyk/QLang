// 1. Alice przygotowuje splątaną parę
state alice, bob;
superpose alice;
entangle alice -> bob;

// 2. Qubit bob przenoszony jest w docelowe miejsce
// (fizycznie lub przez światłowód). W tym czasie 
// nie ma jeszcze w nim żadniej informacji

// 3. Alice chce wysłać wiadomość. Przygotowuje qubit z wiadomością, 
// którego stan może być dowolny.
state msg; // domyślnie stan 0
not msg; // not 0 => qubit przechodzi w stan 1 

// 4. Alice splątuje wiadomość i jej część pary
entangle msg -> alice;

// 5. Rozproszenie informacji z msg do alice
superpose msg;

// 6. Alice wykonuje pomiary
obs m1, m2;
m1 = measure msg;
m2 = measure alice;
// m1 == 1 oznacza, że qubit Boba ma odwróconą fazę
// m2 == 1 oznacza, że qubit Boba ma odwróconą wartość

// 7. Alice przesyła dwa zwykłe bity m1 i m2 do Boba.

// 8. Bob na podstawie otrzymanych wartości m1 i m2
// dokonuje poprawy fazy i wartości qubitu

if(m1 == 1){ // m1 == 1 -> Odwrócenie fazy
    phase_not bob;
}
if(m2 == 1){ // m2 == 1 -> Odwrócenie wartości
    not bob;
}

// 9. Teraz qubit 'bob' jest taki sam jak qubit 'msg'. Bob może 
// dalej prowadzić jakieś operacje na stanie kwantowym lub 
// wykonać pomiar
debug(bob); // wyświetla wewnętrzą reprezentację qubitu
// w realnym świecie podejrzenie stanu qubitu nie jest możliwe