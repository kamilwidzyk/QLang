/*
    Shared utility functions for prime checking.
*/

function is_prime(num n) {
    if(n < 2) {
        return 0;
    }

    num divisor = 2;
    num remainder = 0;
    while(divisor < n) {
        remainder = n;
        while(remainder >= divisor) {
            remainder -= divisor;
        }

        if(remainder == 0) {
            return 0;
        }
        divisor++;
    }

    return 1;
}

function process_prime_check(num current) {
    println("Processing %d" % current);
    num checked = current;
    num prime = is_prime(current);
    return [checked, prime];
}
