// 1. Przygotowanie dwóch niezależnych splątanych par
state alice, bob;
superpose alice;
entangle alice -> bob;

state carol, dave;
superpose carol;
entangle carol -> dave;

// 2. W połowie drogi spotykają się qubity bob i carol
entangle bob -> carol;
superpose bob;

// 3. Pomiar qubitów bob i carol
obs m_bob, m_carol;
m_bob = measure bob;
m_carol = measure carol;

// 4. Korekcja stanu u Dave lub Alice nad podstawie wyników pomiaru
if(m_carol == 1){ 
    not dave; // odwrócenie wartości
}
if(m_bob == 1){
    phase_not dave; // odwrócenie fazy
}

// 5. Teraz qubity alice i dave powinny być splątane
obs res_alice, res_dave;
res_alice = measure alice;
res_dave = measure dave;

print("Wynik pomiaru Alice: ");
println(res_alice);
print("Wynik pomiaru Dave: ");
println(res_dave);

if(res_alice == res_dave){
    println("Wymiana zadziałała");
}else{
    println("Błąd wymiany");
}

// 6. Oba te stany powinny być identyczne
debug(alice);
debug(dave);