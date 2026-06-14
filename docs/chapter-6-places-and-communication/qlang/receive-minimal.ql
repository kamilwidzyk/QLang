place Alice {
    num x = 99;
    send x to Bob;
}

place Bob {
    num x = receive;
    println("Got: %d" % x);
}
