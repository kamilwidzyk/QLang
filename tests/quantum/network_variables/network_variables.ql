place Sender {
    text t1 = "Hello";
    text to_whom = "Receiver";
    text msg_name = "greeting";
    
    send t1 to to_whom as msg_name;
}

place Receiver {
    text expected_sender = "Sender";
    text expected_msg = "greeting";

    text t2 = receive text from expected_sender named expected_msg;

    println(t2);
}
