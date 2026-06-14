num matrix[4][4];            // two-dimensional 4x4 array

// Size inferred automatically from the initialiser
num a[?] = [1, 2, 3, 4, 5]; // size is 5, inferred from the list
println(#a);                 // 5

// Runtime-computed size
num n = 8;
num dynamic[n];              // size determined at runtime
