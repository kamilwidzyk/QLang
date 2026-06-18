place Alice {
    println("Alice is preparing to teleport a qubit to Bob...");
    // Prepera Bell pair
    state q1, q2;
    H q1;
    CNOT q1 -> q2;
    // Send one qubit to Bob
    send q2 to Bob as "qubit";
    println("Bell pair prepared. One qubit sent to Bob.");

    // Get one bit of input from user
    state to_send;
    num flip;
    print("Enter a bit to teleport (0 or 1): ");
    input(flip, 0..1);
    println("Input '%d' received. Preparing qubit to teleport..." % flip);

    // 0 = no change, 1 = apply X gate
    if (flip) X to_send;

    // Prepare qubit to teleport
    CNOT to_send -> q1;
    H to_send;

    // Measure both
    obs measurements[2] = measure [to_send, q1];

    // Send measurement results to Bob
    println("Measurement complete: m0=%d m1=%d" % measurements);
    send measurements to Bob as "measurements";
    println("Measurement results sent to Bob.");
}

place Bob {
    // Receive qubit from Alice (half of Bell pair)
    println("Waiting for qubit from Alice...");
    state q2 = receive state from Alice named "qubit";
    println("Received qubit from Alice.");

    println("Waiting for measurement results from Alice...");
    obs measurements[2] = receive obs from Alice named "measurements";
    println("Received measurement results from Alice.");

    // Apply corrections based on Alice's measurements
    if(measurements[0]) Z q2;
    if(measurements[1]) X q2;

    // q2 should now be in the same state as Alice's original to_send qubit
    println("Teleportation complete.");
    obs orig_state = measure q2;
    println("Original state (0 or 1): %d" % orig_state);
}
