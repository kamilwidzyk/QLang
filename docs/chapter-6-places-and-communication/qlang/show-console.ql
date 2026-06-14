place Worker {
    show_console(0);    // hide console for this place
    num result = 2 ** 10;
    send result to Main as "result";
    show_console(1);    // show console again before exiting
}

place Main {
    num r = receive num from Worker named "result";
    println("Result: %d" % r);
}
