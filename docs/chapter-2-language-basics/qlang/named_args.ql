function rect(num width, num height = 1) {
    return width * height;
}

// Positional arguments
println(rect(5, 3));           // 15

// Mixed: positional + named
println(rect(5, height = 3));  // 15

// All named, any order
println(rect(height = 4, width = 6));  // 24

// Using default value
println(rect(7));              // 7
