place Manager{
    // Manager: dispatch numbers to workers and collect prime results.
    num max_number = 1000; // change as needed
    num primes[?]; // list for collecting primes
    num current_number = 2; // start checking from 2
    // places that will be run as workers
    text workers[?] = ["Worker1", "Worker2", "Worker3", "Worker4"];

    // initial dispatch: send one task to each worker
    iterate workers as worker{
        send current_number to worker as "task";
        current_number++;
    }

    num runningTasks = #workers; // number of tasks currently running
    num next_worker = 0; // this ensures tasks are split evenly

    
    while (runningTasks > 0) {
        // collect the result
        num result[2] = receive num named "result"; // [number, isPrime]
        println("Received: %d -> %d" % result);
        if (result[1] == 1) primes += result[0]; 

        // start new task
        if (current_number <= max_number) {
            text target = workers[next_worker];
            send current_number to target as "task";
            current_number++;
        } else {
            runningTasks--;
        }

        next_worker = (next_worker + 1) % #workers;
    }

    println("Primes found:");
    iterate primes as prime{
        print("%d " % prime);
    }
    println("\nTotal: %d primes." % #primes);

    // Send shutdown signal to workers
    num shutdown_signal = -1;
    iterate workers as worker{
        send shutdown_signal to worker as "task";
    }

    println("Shutdown signals sent to workers. Manager exiting.");

}

// 4 workers, each gets the same code to run
place Worker1{
    <<""worker_code.ql"">>;
}

place Worker2{
    <<""worker_code.ql"">>;
}

place Worker3{
    <<""worker_code.ql"">>;
}

place Worker4{
    <<""worker_code.ql"">>;
}

