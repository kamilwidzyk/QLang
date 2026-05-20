num first = seed(123); // set seed to 123 and return the new seed(now its 123)
println("%d" % first); // 123
println("%d" % seed()); // seed getter: returns 123
seed(456); // set seed to 456
println("%d" % seed()); // seed getter: now it should be 456
