place Alice {
    num x = 10;
    text msg = "hello";

    // Full form: target and name
    send x to Bob as "number";

    // Target only, no name
    send msg to Bob;

    // Name only, no target, any place can receive
    send x as "data";
}
