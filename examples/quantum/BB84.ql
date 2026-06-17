// Demonstrates BB84 protocol
// Alice and Bob exchange key information via a channel
// that was intercepted by a middle-man Eve spy(she will try
// to steal qubits and resend them, which will be detected by Alice and Bob)
//
// Alice and Bob will have the same sectet key if the channel is secure
// otherwise they will detect the interception
//
//

place Alice{
    <<"stdlib:random.ql">>;
    <<"stdlib:utils.ql">>;

    // QUANTUM TRANSMISSION
    const num n_qubits = 64; // Amount of transmitted qubits
    obs bits[?] = random_bits(count=n_qubits);
    obs bases[?] = random_bits(count=n_qubits); // 0=Z 1=X
    state q[n_qubits]; // qubits to send

    for i from 0 to n_qubits{
        // Encode bits
        if(bits[i]) X q[i]; 
        // Encode basis
        if(bases[i]) H q[i];
    }

    println("Number of qubits: %d" % n_qubits);
    println("My bits: %s" % binary_to_str(bits));
    println("My bases: %s" % binary_to_str(bases, zero="Z", one="X"));

    send q to Eve_spy as "qubits"; // send to spy(simulated interception)
    println("Qubits sent. Waiting for bases from Bob...");

    // EXCHANGE OF BASES (not secret)
    obs bob_bases[?] = receive obs from Bob named "bob_bases";
    println("Received bases from Bob: %s" % binary_to_str(bob_bases, zero="Z", one="X"));
    send bases to Bob as "alice_bases";
    println("Sent my bases to Bob.");

    // MAKE A SECRET KEY
    obs key[?] = [];

    for i from 0 to n_qubits{
        if(bases[i] == bob_bases[i]) key += bits[i];
    }

    println("My secret key: %s" % binary_to_str(key));

    // QUBIT ANTI-TAMPER CHECK
    const num sample_size = cut(#key / 2); 
    println("Sample size: %d" % sample_size);

    obs key_sample[?] = key[0..sample_size];
    println("My sample bits: %s" % binary_to_str(key_sample));
    
    send key_sample to Bob as "key_sample";
    println("Sent key sample to Bob. ");

    println("Waiting for error_rate from Bob...");
    num error_rate = receive num from Bob named "error_rate";

    println("Error rate is: %.4f" % error_rate);
    println(error_rate > 0.11 ? "Channel not secure, qubits altered." : "Channel secure.");
}

place Eve_spy{
    <<"stdlib:random.ql">>;
    <<"stdlib:utils.ql">>;

    // T = Eve steals qubits, F = Eve sends qubits untouched
    const obs steal_qubits = F;

    while(T){
        state q[?] = receive state named "qubits";
        
        // Spying disabled, send as nothing happend
        if(!steal_qubits){ 
            println("Sending %d qubits untouched." % #q);
            send q to Bob as "qubits"; 
            continue; 
        }
        
        println("%d qubits stolen." % #q);
        obs guessed_basis[?] = random_bits(count=#q);
        println("Guessed basis: %s" % binary_to_str(guessed_basis, zero="Z", one="X"));

        // Apply guessed basis to stolen qubits
        for i from 0 to #q{
            if(guessed_basis[i]) H q[i];
        }

        // Measure stolen qubits -> original states collapse
        obs measured[?] = measure q; 
        println("Measured bits: %s" % binary_to_str(measured));

        // Create the same amount of qubits to send back
        state q_fake[#q]; 
        
        // Encode the "same" information on fake ones
        for i from 0 to #q{
            if(measured[i]) X q_fake[i]; // Encode bit
            if(guessed_basis[i]) H q_fake[i]; // Encode basis
        }

        // Send packet back on it's way
        send q_fake to Bob as "qubits";
    }
}

place Bob{
    <<"stdlib:random.ql">>;
    <<"stdlib:utils.ql">>;

    const num n_qubits = 64; // Amount of qubits
    obs bases[?] = random_bits(count=n_qubits); // 0=Z 1=X

    println("My bases: %s" % (binary_to_str(bases, zero="Z", one="X")));
    println("Waiting for qubits...");

    // RECEIVED QUBITS MEASUREMENT
    state q[?] = receive state named "qubits";
    
    // Apply Bob's bases
    for i from 0 to n_qubits{
        if(bases[i]) H q[i];
    }

    // Measure all
    obs bits[?] = measure q;
    println("My bits: %s" % binary_to_str(bits));

    // EXCHANGE OF BASES (not secret)
    send bases to Alice as "bob_bases";
    println("Sent bases to Alice. Waiting for bases from Alice...");
    obs alice_bases[?] = receive obs named "alice_bases";
    println("Received bases from Alice: %s" % binary_to_str(alice_bases, zero="Z", one="X"));

    // MAKE A SECRET KEY
    obs key[?] = [];
    
    for i from 0 to n_qubits{
        if(bases[i] == alice_bases[i]) key += bits[i];
    }

    println("My secret key: %s" % binary_to_str(key));

    // WAIT FOR KEY SAMPLE
    println("Waiting for key sample from Alice...");
    obs alice_key_sample[?] = receive obs named "key_sample";
    const num sample_size = cut(#key / 2);

    println("Received key sample: %s" % binary_to_str(alice_key_sample));

    // check for errors
    num errors = 0;
    for i from 0 to sample_size{
        if(key[i] != alice_key_sample[i]) errors++;
    }

    num error_rate = errors / sample_size;

    send error_rate to Alice as "error_rate";
    println("Sent error_rate to Alice.");

    println("Error rate is: %.4f" % error_rate);
    println(error_rate > 0.11 ? "Channel not secure, qubits altered." : "Channel secure.");
}
