const obs MAX_SIZE[8] = 100;   // sized obs constant
const num EPSILON = 0.0001;    // num constant

num x = 10;
x++;       // still mutable
const x;   // freeze: further assignments raise an error
