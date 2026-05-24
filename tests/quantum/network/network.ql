place Alice {
    state qubit;
    X qubit;
    send qubit to Bob as "alice-qubit";

    obs flag = 1;
    send flag to Bob as "alice-flag";

    num numbers[3] = [7, 8, 9];
    send numbers to Bob as "alice-numbers";

    text greeting = "hello network";
    send greeting to Bob as "alice-greeting";
};

place Carol {
    num answer = 42;
    send answer to Bob as "carol-answer";

    text open = "broadcast";
    send open as "open-text";
};

place Bob {
    state received_qubit = receive state from Alice named "alice-qubit";
    obs measured_qubit = measure received_qubit;
    println("[state/from+named]", measured_qubit);

    obs received_flag = receive obs named "alice-flag";
    println("[obs/named-only]", received_flag);

    num received_numbers[3] = receive num from Alice named "alice-numbers";
    println("[num-list/from+named]", received_numbers);

    num received_answer = receive num from Carol named "carol-answer";
    println("[num/from+named]", received_answer);

    text received_greeting = receive text named "alice-greeting";
    println("[text/named-only]", received_greeting);

    text received_open = receive text from Carol;
    println("[text/from-only]", received_open);
};
