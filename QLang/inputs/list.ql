println("Test listy 10 elementów");
num a[10] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
print("Długość listy: ");
println(#a);
print("Indeks 0: ");
println(a[0]);
print("Indeks 2: ");
println(a[2]);

println();
println("Test tablicy 3x3x3");
num b[3][3][3] = [
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
    [
        [10, 11, 12],
        [13, 14, 15],
        [16, 17, 18]
    ],
    [
        [19, 20, 21],
        [22, 23, 24],
        [25, 26, 27]
    ]
];
print("Długość tablicy: ");
println(#b);
println(b);
println("Iteracja po elementach tablicy");
for i from 0 to #b {
    print("Indeks: ");
    println(i);
    print("Wartość: ");
    println(b[i]);
}
