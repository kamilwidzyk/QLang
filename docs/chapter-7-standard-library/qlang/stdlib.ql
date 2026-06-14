// Set random seed
seed(12345);

// Get a random float [0, 1)
num r = random();

// Math rounding and truncating functions
num val = 12.3456;

num c = cut(val, 2);      // 12.34
num f = floor(val, 1);    // 12.3
num cl = ceil(val, 0);    // 13
num rnd = round(val, 3);  // 12.346
