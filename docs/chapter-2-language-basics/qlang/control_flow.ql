obs x[8] = 75;

if (x > 100) {
    println("Large");
} else if (x > 50) {
    println("Medium");
} else {
    println("Small");
}

// For loop with step
for i from 0 to 20 step 5 {
    println(i);      // 0, 5, 10, 15
}

// While loop
obs n[8] = 1;
while (n < 128) {
    n *= 2;
}
println(n);          // 128
