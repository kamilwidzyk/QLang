<<"stdlib:random.ql">>

// Test random int
println("Random ints 0-10:");
for i from 0 to 5{
    num n = random_int(0, 10);
    println("\t%d" % n);
}

// Test random float
println("Random floats 0-10:");
for i from 0 to 5{
    num n = random_float(0, 10);
    println("\t%.4f" % n);
}

// Test random range
println("Random range 0-100 step 5");
for i from 0 to 5{
    num n = random_range(0, 100, 5);
    println("\t%.2f" % n);
}

// Test random choice
println("Random choice from list");
for i from 0 to 5{
    num n = random_choice([1, 2, 3.14, 6, 7]);
    println("\t%.2f" % n);
}

println("Random choice from arguments");
for i from 0 to 5{
    println("\t" + random_choice_args("one", 3.14, "pi", 123));
}

println("Random list of 5 ints 0-100");
for i from 0 to 5{
    println("\t" + random_list(
        list_size = 5,
        min_val = 0,
        max_val = 100,
        only_int = T
    ));
}

println("Random list of 5 floats 0-5");
for i from 0 to 5{
    println("\t" + random_list(
        list_size = 5,
        min_val = 0,
        max_val = 5
    ));
}

println("Random list of 16 bits");
for i from 0 to 5{
    println("\t" + random_bits(16));
}