place Alice {
    state a, b;
    H a;
    CNOT a -> b;
    obs ma = measure a;
    obs mb = measure b;
    println("Measurement A: %d" % ma);
    println("Measurement B: %d" % mb);
    state qs[2];
    X qs[1];
    obs mc = measure qs[1];
    println("Measurement Q1: %d" % mc);
}
