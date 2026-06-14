// Convert an array of bits to an integer
// The first element is the Least Significant Bit (LSB)
num bits[?] = [1, 0, 1];     // 1*2^0 + 0*2^1 + 1*2^2 = 1 + 4 = 5
num val = bits >> num;       // val is 5

// Convert an integer to an array of observation bits
// Extracts the given number of bits (4 in this case)
obs out[4] = 5 > 4 > obs;    // out is [1, 0, 1, 0]
