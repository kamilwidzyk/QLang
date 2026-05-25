num numbers[?] = [10, 20, 30, 40, 50];

iterate numbers as n {
    println(n);
} // 10\n20\n30\n40\n50\n

iterate numbers as n index i{
    println("%d: %d" % [i, n]);
} // 0: 10\n1: 20\n2: 30\n3: 40\n4: 50\n

text fruits[?] = ["apple", "banana", "cherry"];
iterate fruits as fruit{
    println(fruit);
} // apple\nbanana\ncherry\n

function returnMixedList(){
    return ["text", 123, [1, "b"]];
}

iterate returnMixedList() as elem {
    println(elem);
} // text\n123\n[1, 'b']\n

// expected output: 10\n20\n30\n40\n50\n0: 10\n1: 20\n2: 30\n3: 40\n4: 50\napple\nbanana\ncherry\ntext\n123\n[1, 'b']\n
