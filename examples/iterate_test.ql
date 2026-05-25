println("Test iterate loop");

num numbers[5] = [10, 20, 30, 40, 50];

println("Iterating over numbers:");
iterate numbers as value {
    println(value);
}

println();
println("Iterating with index:");
iterate numbers as n index idx {
    print("Index: ");
    println(idx);
    print("Value: ");
    println(n);
}

println();
println("Test with text array:");
text fruits[3] = ["apple", "banana", "cherry"];
iterate fruits as fruit {
    println(fruit);
}
