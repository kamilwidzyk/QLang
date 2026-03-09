// 1. Dwa bity do przesłania wczytane od użytkownika
obs data[2];
print("Wprowadź dwa bity: ");
input(data, BIN);
print("\n");

// 2. Przygotowanie splądanej pary. Każdy dostaje jedną cześć pary.
state alice, bob;
superpose alice;
entangle alice -> bob;

// 3. Alice koduje 2 bity na swoim qubicie
if(data[0] == 1){ // Pierwszy bit kodowany jako wartość
    not alice; 
}
if(data[1] == 1){ // Drugi bit kodowant jako faza
    phase_not alice;
}

// 4. Alice przesyła qubit do Boba
entangle alice -> bob;
superpose alice;

// 5. Bob mierzy oba kubity
obs result[2];
result[0] = measure alice;
result[1] = measure bob;

print("Odebrane bity: ");
print(result);
print("\n");