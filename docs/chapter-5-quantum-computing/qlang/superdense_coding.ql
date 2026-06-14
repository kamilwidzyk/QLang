place Alice{
    // Prepare entangled pair and send one qubit to Bob
    state qA, qB;
    H qA;
    CNOT qA -> qB;
    send qB to Bob as "qubitB";

    // Get two bits of input from user
    obs bits[2];
    print("Enter number 0-3 (two bits): ");
    input(bits, 0..3);
    println("Input '%d' received. Preparing qubit to send..." % bits);
    println("Bits to send: %d %d" % [bits[0], bits[1]]);

    // Encode the two bits into the qubit
    if (bits[0]) Z qA; // Flip phase for bit 0
    if (bits[1]) X qA; // Flip bit for bit 1

    // Send the encoded qubit to Bob
    send qA to Bob as "qubitA";
    println("Encoded qubit sent to Bob.");
}

place Bob {
    println("Bob is waiting for qubits from Alice...");
    state qB = receive state from Alice named "qubitB";
    println("Received first qubit from Alice.");
    state qA = receive state from Alice named "qubitA";
    println("Received second qubit from Alice.");

    // Decode the received qubits
    CNOT qA -> qB;
    H qA;
    obs result[?] = measure [qA, qB];
    println("Measurement complete. Decoded bits: %d %d" % [result[0], result[1]]);
    println("Decoded number: %d" % result);
}
