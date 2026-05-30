place Alice {
    packet_log(1);  // enable packet logging
    num x = 42;
    send x to Bob as "value";
    packet_log(0);  // disable packet logging
}

place Bob {
    packet_log(1);
    num x = receive num from Alice named "value";
    println("Got: %d" % x);
}
