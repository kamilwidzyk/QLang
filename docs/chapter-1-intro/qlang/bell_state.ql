place Alice {
    state a, b;

    H a;           // Put qubit 'a' into superposition
    CNOT a -> b;   // Entangle 'a' with 'b' — this creates a Bell state

    obs ma = measure a;
    obs mb = measure b;

    println("Measurement A: %d" % ma);
    println("Measurement B: %d" % mb);
    // Both will always agree: both 0 or both 1
}
