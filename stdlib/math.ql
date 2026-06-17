// Returns absolute value of a number
function abs(num x) {
    return x < 0 ? -x : x;
}

// Returns minimum of all given numbers
function minimum(...nums) {
    num result = 0;
    obs first = T;
    iterate nums as n {
        if(first){
            first = F;
            result = n;
        }else result = n < result ? n : result;
    }
    return result;
}

// Returns maximum of all given numbers
function maximum(...nums) {
    num result = 0;
    obs first = T;
    iterate nums as n {
        if(first){
            first = F;
            result = n;
        }else result = n > result ? n : result;
    }
    return result;
}

// Returns T if number is prime, F is not
function is_prime(num n) {
	num i = 2;
	while (i**2 <= n) {
		if (n % i++ == 0) return F;
	}
	return T;
}

// Returns factorial of a given number
function factorial(num n) {
    if (n == 0) return 1;
    return n*factorial(n-1);
}
