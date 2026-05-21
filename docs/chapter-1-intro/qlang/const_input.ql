const obs MAX_SIZE[8] = 100;
const num EPSILON = 0.0001;

obs age[8];
input(age);                   // read any value

obs score[8];
input(score, 0..100);         // accept only values in [0, 100]
