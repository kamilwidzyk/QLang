// Receives a number to check from the Manager and sends back [number, isPrime]

show_console(0); // hide console for workers

// return 1 if n is prime, else 0
function is_prime(num n) {
	num i = 2;
	while (i**2 <= n) {
		if (n % i++ == 0) return 0;
	}
	return 1;
}

num processed;

// worker loop that runs until a shutdown signal is received
while (T) {
	num task = receive num from Manager named "task";
    if(task == -1) break; // stop loop at shutdown signal
    
    println("Worker received task: %d" % task);
	num prime = is_prime(task);
	num result[2] = [task, prime];
    println("Worker sending result: %d -> %d" % [task, prime]);
	send result to Manager as "result";
	processed++;
}
println("Worker processed %d tasks." % processed);
println("Worker received shutdown signal. Exiting.");
show_console(1); // show the console again before exiting
