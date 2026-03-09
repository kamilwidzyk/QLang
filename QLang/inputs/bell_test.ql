state q[2];
obs res[2];

// 1. Generowanie splątania
superpose q[0];
entangle q[0] -> q[1];

// 2. Pomiar wartości obu qubitów
res = measure q;

print("Wynik pomiaru pary Bella:");
println(res);

if(res[0] == res[1]){
    println("Wyniki są identyczne, koleracja zachowana");
}