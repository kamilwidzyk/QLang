obs age[8];
input(age);                   // read any value

obs score[8];
input(score, 0..100);         // accept only values in range [0, 100]
input(score, range(0, 100));  // equivalent syntax

