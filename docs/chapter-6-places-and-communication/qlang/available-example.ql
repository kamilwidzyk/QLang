place Alice {
    for i from 0 to 5 {
        num x = (i * 19) % 13;
        wait(1 second); // simulate heavy computation
        send x to Bob as "number";
    }
    text status = "done";
    send status to Bob as "status";
}

place Bob {
    function receive_numbers() {
        num numbers[5];
        for i from 0 to 5 {
            num x = receive num from Alice;
            numbers[i] = x;
        }
        return numbers;
    }

    obs running = T;

    while(running){
        wait(100 ms); // avoid high CPU load
        if (available text named "status"){
            text status = receive text named "status";
            println(receive_numbers());
            running = F;
        }
    }
}
