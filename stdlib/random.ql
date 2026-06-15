// Useful function for creating random numbers and list

<<"stdlib:math.ql">>;

// Returns a random float in range [min_val, max_val)
function random_float(num min_val = 0, num max_val = 1){
    num rnd = random(); // 0-1
    rnd *= abs(max_val - min_val);
    rnd += min_val;
    return rnd;
}


// Returns an integer in range [min_val, max_val)
function random_int(num min_val = 0, num max_val = 100){
    return cut(random_float(min_val, max_val));
}

// Returns a float in range [min_val, max_val) with a given step
function random_range(num min_val = 0, num max_val = 1, num step_size = 0.1){
    num rnd = random(); // 0-1
    const num n_values = ceil((max_val - min_val) / step_size);
    const num idx = random_int(max_val=n_values);
    return min_val + idx * step_size;
}

// Returns a random element from a given list
function random_choice(any list){
    const num idx = random_int(max_val=#list);
    return list[idx];
}

// Returns a random argument
function random_choice_args(...args){
    const num idx = random_int(max_val=#args);
    return args[idx];
}

// Returns a list of random values
function random_list(num list_size, num min_val = 0, num max_val = 100, obs only_int = F){
    num result[list_size];
    for i from 0 to list_size{
        result[i] = (only_int ? random_int(min_val, max_val) : random_float(min_val, max_val));
    }
    return result;
}

// Returns a list of random 0/1 bits
function random_bits(num count){
    return random_list(
        list_size = count,
        min_val = 0,
        max_val = 2, // yes, 2, end is exclusive
        only_int = T
    );
}
