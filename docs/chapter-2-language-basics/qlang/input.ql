obs age[8];
input(age);                   // read any integer

obs score[8];
input(score, 0..100);         // accept only values in [0, 100]
input(score, range(0, 100));  // equivalent form
