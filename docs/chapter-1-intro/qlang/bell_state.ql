place Alice {
    state a, b;

    superpose a;           // Put qubit 'a' into superposition
    entangle a -> b;       // Entangle 'a' with 'b' to create a Bell state

    obs ma = measure a;
    obs mb = measure b;

    println("Measurement A: %d" % ma);
    println("Measurement B: %d" % mb);
}