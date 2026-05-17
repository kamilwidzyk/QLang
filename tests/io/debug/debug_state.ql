place Alice {
    state s;
    H s;
    X s;
    debug(@s);
    
    state q[2];
    H q[0];
    CNOT q[0] -> q[1];
    debug(@q);
}
