// This file in included as code in all workers.
// This file cannot contain any place declaration, only the main code can.

// Worker code used by all workers.
// Receives a number to check from the Manager and sends back [number, isPrime]

<<"stdlib:math.ql">>;

show_console(0); // hide console for workers

num processed;

// worker loop that runs until a shutdown signal is received
while (T) {
	num task = receive num from Manager named "task";
    if(task == -1) break; // stop loop at shutdown signal
    
    println("Worker received task: %d" % task);
	num result[?] = [task, is_prime(task)];
    println("Worker sending result: %d -> %d" % result);
	send result to Manager as "result";
	processed++;
}
println("Worker processed %d tasks." % processed);
println("Worker received shutdown signal. Exiting.");
show_console(1); // show the console again before exiting