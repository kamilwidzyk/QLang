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
