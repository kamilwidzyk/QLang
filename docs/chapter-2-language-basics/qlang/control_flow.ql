num x = 75;

if (x > 100) {
    println("Large");
} else if (x > 50) {
    println("Medium");
} else {
    println("Small");
}

// if without braces
if (x > 0) println("Positive");

// Ternary operator
text label = x > 50 ? "big" : "small";
println(label);

// For loop with step
for i from 0 to 20 step 5 {
    println(i);      // 0, 5, 10, 15
}

// While loop
num n = 1;
while (n < 128) {
    n *= 2;
}
println(n);          // 128
